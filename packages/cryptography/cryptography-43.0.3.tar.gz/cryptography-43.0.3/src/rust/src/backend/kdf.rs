// This file is dual licensed under the terms of the Apache License, Version
// 2.0, and the BSD License. See the LICENSE file in the root of this repository
// for complete details.

use crate::backend::hashes;
use crate::buf::CffiBuf;
use crate::error::CryptographyResult;

#[pyo3::pyfunction]
pub(crate) fn derive_pbkdf2_hmac<'p>(
    py: pyo3::Python<'p>,
    key_material: CffiBuf<'_>,
    algorithm: &pyo3::Bound<'_, pyo3::PyAny>,
    salt: &[u8],
    iterations: usize,
    length: usize,
) -> CryptographyResult<pyo3::Bound<'p, pyo3::types::PyBytes>> {
    let md = hashes::message_digest_from_algorithm(py, algorithm)?;

    Ok(pyo3::types::PyBytes::new_bound_with(py, length, |b| {
        openssl::pkcs5::pbkdf2_hmac(key_material.as_bytes(), salt, iterations, md, b).unwrap();
        Ok(())
    })?)
}

#[cfg(not(CRYPTOGRAPHY_IS_LIBRESSL))]
#[pyo3::pyfunction]
#[allow(clippy::too_many_arguments)]
fn derive_scrypt<'p>(
    py: pyo3::Python<'p>,
    key_material: CffiBuf<'_>,
    salt: &[u8],
    n: u64,
    r: u64,
    p: u64,
    max_mem: u64,
    length: usize,
) -> CryptographyResult<pyo3::Bound<'p, pyo3::types::PyBytes>> {
    Ok(pyo3::types::PyBytes::new_bound_with(py, length, |b| {
        openssl::pkcs5::scrypt(key_material.as_bytes(), salt, n, r, p, max_mem, b).map_err(|_| {
            // memory required formula explained here:
            // https://blog.filippo.io/the-scrypt-parameters/
            let min_memory = 128 * n * r / (1024 * 1024);
            pyo3::exceptions::PyMemoryError::new_err(format!(
                "Not enough memory to derive key. These parameters require {min_memory}MB of memory."
            ))
        })
    })?)
}

#[pyo3::pymodule]
pub(crate) mod kdf {
    #[pymodule_export]
    use super::derive_pbkdf2_hmac;
    #[cfg(not(CRYPTOGRAPHY_IS_LIBRESSL))]
    #[pymodule_export]
    use super::derive_scrypt;
}
