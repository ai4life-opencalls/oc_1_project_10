import numpy as np
import flowkit as fk
from scipy.spatial import ConvexHull

from tqdm.notebook import tqdm

from logicle_scaling import LogicleTransform


SEED = 7
np.random.seed(SEED)


def get_bin_centers(high_sim_data):
    hist, x_edges, y_edges = np.histogram2d(
        high_sim_data[:, 1], high_sim_data[:, 0],
        bins=(300, 300), density=False
    )
    hist = hist.T
    hist_threshold = np.quantile(hist[hist > 0].ravel(), 0.05)
    hist_mask = np.zeros_like(hist).astype(bool)
    hist_mask[hist > hist_threshold] = 1
    y_centers = (y_edges[:-1] + y_edges[1:]) / 2
    x_centers = (x_edges[:-1] + x_edges[1:]) / 2
    xx, yy = np.meshgrid(x_centers.ravel(), y_centers.ravel())
    # get centers as y,x coords
    bin_centers = np.stack(
        [yy.ravel(), xx.ravel()], axis=1
    ).reshape(len(y_centers), len(x_centers), -1)
    masked_bin_centers = bin_centers[hist_mask]

    return masked_bin_centers


def get_centroid(polygon):
    # Same polygon, but with vertices cycled around. Now the polygon
    # decomposes into triangles of the form origin-polygon[i]-polygon2[i]
    polygon2 = np.roll(polygon, -1, axis=0)
    # Compute signed area of each triangle
    signed_areas = 0.5 * np.cross(polygon, polygon2)
    # Compute centroid of each triangle
    centroids = (polygon + polygon2) / 3.0
    # Get average of those centroids, weighted by the signed areas.
    centroid = np.average(centroids, axis=0, weights=signed_areas)

    return centroid


def scale_polygon(polygon, scale):
    centroid = get_centroid(polygon)
    scaled_polygon = (scale * (polygon - centroid)) + centroid

    return scaled_polygon


def inverse_logicle(logicle_data, logicle_params):
    original_data = np.zeros_like(logicle_data)
    logicle = LogicleTransform(
        top_of_scale=logicle_params[0, 0],
        m_positive_decades=logicle_params[0, 1],
        width_of_linear=logicle_params[0, 2],
        addition_negative=logicle_params[0, 3]
    )
    original_data[:, 0] = logicle.inverse(logicle_data[:, 0])

    logicle = LogicleTransform(
        top_of_scale=logicle_params[1, 0],
        m_positive_decades=logicle_params[1, 1],
        width_of_linear=logicle_params[1, 2],
        addition_negative=logicle_params[1, 3]
    )
    original_data[:, 1] = logicle.inverse(logicle_data[:, 1])

    return original_data


def get_logicle_polygon_gates(df_pairs, df_positive, high_sim_mask):
    pair_polygons = []
    total_pairs = len(df_pairs)
    for i, row in tqdm(
        df_pairs.iterrows(), total=total_pairs,
        desc="Calculate pairs' polygon gates (logicle)"
    ):
        pair = row[["channel_1", "channel_2"]].to_list()
        data = df_positive[pair].to_numpy()
        high_sim_data = data[high_sim_mask]
        high_sim_bin_centers = get_bin_centers(high_sim_data)
        try:
            # get convex hull polygon
            hull = ConvexHull(high_sim_bin_centers)
            polygon = high_sim_bin_centers[hull.vertices]
            # scaled_polygon = scale_polygon(polygon, 1.1)
        except Exception:
            polygon = None

        pair_polygons.append(polygon)

    return pair_polygons


def get_gating_startegy(pair, polygon):
    gating = fk.GatingStrategy()
    parents = ["root"]

    dim1 = fk.Dimension(pair[0])
    dim2 = fk.Dimension(pair[1])
    gate = fk.gates.PolygonGate(
        gate_name="g1", dimensions=[dim1, dim2],
        vertices=polygon.tolist()
    )
    gating.add_gate(gate, tuple(parents))

    return gating


def get_gate_stats(gate_polygon, df_positive, df_negative):
    pair = df_positive.columns.to_list()
    gating = get_gating_startegy(pair, gate_polygon)
    samples = [
        fk.Sample(df_positive, sample_id="positive"),
        fk.Sample(df_negative, sample_id="negative")
    ]
    session = fk.Session(
        gating_strategy=gating,
        fcs_samples=samples
    )
    session.analyze_samples(use_mp=True, verbose=False)
    df_report = session.get_analysis_report()
    positive_mask = df_report["sample"] == "positive"
    tp = df_report[positive_mask]["count"].sum()
    fp = df_report[~positive_mask]["count"].sum()

    return tp, fp


def get_pair_precisions(
    df_pairs, logicle_polygons, df_logicle_params,
    df_positive, df_negative
):
    results = {
        "channel_1": [],
        "channel_2": [],
        "precision": [],
        "TP": [],
        "FP": []
    }

    for i, row in tqdm(
        df_pairs.iterrows(), total=len(df_pairs), desc="Calculate gate precisions"
    ):
        logicle_polygon = logicle_polygons[i]
        pair = row[["channel_1", "channel_2"]].to_list()
        results["channel_1"].append(pair[0])
        results["channel_2"].append(pair[1])

        if logicle_polygon is not None:
            logicle_params = df_logicle_params.loc[pair].to_numpy()
            data_polygon = inverse_logicle(logicle_polygon, logicle_params)
            # get gate stats for current pair (channels) in original data scales
            tp, fp = get_gate_stats(
                data_polygon,
                df_positive[pair], df_negative[pair]
            )
            results["TP"].append(tp)
            results["FP"].append(fp)
            # precision
            precision = round(tp * 100 / (tp + fp), 2)
            results["precision"].append(precision)
        else:
            results["TP"].append(-1)
            results["FP"].append(-1)
            results["precision"].append(-1)

    df_result = df_pairs.copy()
    df_result["precision"] = results["precision"]
    df_result["TP"] = results["TP"]
    df_result["FP"] = results["FP"]

    return df_result.sort_values("precision", ascending=False).reset_index(drop=True)
