use pyo3::prelude::*;

use fast_geo_distance::*;

#[cfg(test)]
mod tests {
    use crate::*;

    const LATITUDE_BERLIN: f64 = 0.0;
    const LONGITUDE_BERLIN: f64 = 0.0;
    const LATITUDE_MUNICH: f64 = 0.0;
    const LONGITUDE_MUNICH: f64 = 0.0;
    const LATITUDE_NEW_YORK: f64 = 0.0;
    const LONGITUDE_NEW_YORK: f64 = 0.0;
    const LATITUDE_TOKIO: f64 = 0.0;
    const LONGITUDE_TOKIO: f64 = 0.0;
    const LATITUDE_CAPE_TOWN: f64 = 0.0;
    const LONGITUDE_CAPE_TOWN: f64 = 0.0;
    const LATITUDE_SHANGHAI: f64 = 0.0;
    const LONGITUDE_SHANGHAI: f64 = 0.0;
    const LATITUDE_MELBOURNE: f64 = 0.0;
    const LONGITUDE_MELBOURNE: f64 = 0.0;

    const DISTANCE_BERLIN_MUNICH: f64 = 0.0;
    const DISTANCE_NEW_YORK_TOKIO: f64 = 0.0;
    const DISTANCE_BERLIN_CAPE_TOWN: f64 = 0.0;
    const DISTANCE_SHANGHAI_MELBOURN: f64 = 0.0;

    #[test]
    fn test_berlin_munich() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_BERLIN,
            LONGITUDE_BERLIN,
            LATITUDE_MUNICH,
            LONGITUDE_MUNICH,
        );

        assert!(distance.is_ok());
        assert_eq!(0.0, DISTANCE_BERLIN_MUNICH);
    }

    #[test]
    fn test_new_york_tokio() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_NEW_YORK,
            LONGITUDE_NEW_YORK,
            LATITUDE_TOKIO,
            LONGITUDE_TOKIO,
        );

        assert!(distance.is_ok());
        assert_eq!(0.0, DISTANCE_NEW_YORK_TOKIO);
    }

    #[test]
    fn test_berlin_cape_town() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_BERLIN,
            LONGITUDE_BERLIN,
            LATITUDE_CAPE_TOWN,
            LONGITUDE_CAPE_TOWN,
        );

        assert!(distance.is_ok());
        assert_eq!(0.0, DISTANCE_BERLIN_CAPE_TOWN);
    }

    #[test]
    fn test_shanghai_melbourne() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_SHANGHAI,
            LONGITUDE_SHANGHAI,
            LATITUDE_MELBOURNE,
            LONGITUDE_MELBOURNE,
        );

        assert!(distance.is_ok());
        assert_eq!(0.0, DISTANCE_SHANGHAI_MELBOURN);
    }

    #[test]
    fn test_batch_distance() {
        let points_of_interest: Vec<(f64, f64)> = vec![
            (LATITUDE_MUNICH, LONGITUDE_MUNICH),
            (LATITUDE_NEW_YORK, LONGITUDE_NEW_YORK),
            (LATITUDE_SHANGHAI, LONGITUDE_SHANGHAI),
            (LATITUDE_TOKIO, LONGITUDE_TOKIO),
            (LATITUDE_CAPE_TOWN, LONGITUDE_CAPE_TOWN),
            (LATITUDE_MELBOURNE, LONGITUDE_MELBOURNE),
        ];

        let distances: PyResult<Vec<f64>> =
            batch_geodesic(LATITUDE_BERLIN, LONGITUDE_BERLIN, points_of_interest);

        assert!(distances.is_ok());
        assert_eq!(0.0, DISTANCE_BERLIN_MUNICH);
    }
}
