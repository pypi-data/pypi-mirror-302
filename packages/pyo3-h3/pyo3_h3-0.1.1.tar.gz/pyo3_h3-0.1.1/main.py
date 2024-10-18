import polars as pl
from pyo3_h3 import parallel_lat_lon_to_cell


H3_RESOLUTION = 10


def main():
    data = {
        "latitude": [48.06310367302714, 48.448324429734946, 52.5336711389146],
        "longitude": [11.533139985449772, 10.859384015093356, 13.376248789933639],
    }
    df = pl.DataFrame(
        data, schema=[("latitude", pl.Float64), ("longitude", pl.Float64)]
    )

    df_h3_cell = parallel_lat_lon_to_cell(
        df,
        "latitude",
        "longitude",
        H3_RESOLUTION,
        "h3_cell",
    )

    print(df_h3_cell)


if __name__ == "__main__":
    main()
