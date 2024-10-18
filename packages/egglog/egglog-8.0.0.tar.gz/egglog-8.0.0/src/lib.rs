mod conversions;
mod egraph;
mod error;
mod py_object_sort;
mod serialize;
mod utils;

use conversions::{Expr, Span, Term, TermDag};
use pyo3::prelude::*;

#[pyfunction]
fn termdag_term_to_expr(termdag: &TermDag, term: Term) -> Expr {
    let termdag: egglog::TermDag = termdag.into();
    let term: egglog::Term = term.into();
    termdag.term_to_expr(&term).into()
}

/// Bindings for egglog rust library
#[pymodule]
fn bindings(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    pyo3_log::init();

    let dummy: Span = egglog::ast::DUMMY_SPAN.clone().into();
    m.add("DUMMY_SPAN", dummy)?;
    m.add_class::<crate::py_object_sort::ArcPyObjectSort>()?;
    m.add_class::<crate::serialize::SerializedEGraph>()?;
    m.add_class::<crate::egraph::EGraph>()?;
    m.add_class::<crate::error::EggSmolError>()?;
    m.add("HIGH_COST", egglog::HIGH_COST)?;
    m.add_function(wrap_pyfunction!(termdag_term_to_expr, m)?)?;

    crate::conversions::add_structs_to_module(m)?;
    crate::conversions::add_enums_to_module(m)?;

    Ok(())
}
