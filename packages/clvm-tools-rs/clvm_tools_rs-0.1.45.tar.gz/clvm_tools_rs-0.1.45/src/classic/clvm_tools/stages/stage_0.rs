use clvm_rs::allocator::{Allocator, NodePtr};
use clvm_rs::chia_dialect::{ChiaDialect, ENABLE_BLS_OPS_OUTSIDE_GUARD, NO_UNKNOWN_OPS};
use clvm_rs::cost::Cost;
use clvm_rs::reduction::Response;

use clvm_rs::run_program::{run_program_with_pre_eval, PreEval};

#[derive(Default)]
pub struct RunProgramOption {
    pub max_cost: Option<Cost>,
    pub pre_eval_f: Option<PreEval>,
    pub strict: bool,
    pub new_operators: bool,
}

pub trait TRunProgram {
    fn run_program(
        &self,
        allocator: &mut Allocator,
        program: NodePtr,
        args: NodePtr,
        option: Option<RunProgramOption>,
    ) -> Response;
}

pub struct DefaultProgramRunner {}

impl DefaultProgramRunner {
    pub fn new() -> Self {
        DefaultProgramRunner {}
    }
}

impl Default for DefaultProgramRunner {
    fn default() -> Self {
        DefaultProgramRunner::new()
    }
}

impl TRunProgram for DefaultProgramRunner {
    fn run_program(
        &self,
        allocator: &mut Allocator,
        program: NodePtr,
        args: NodePtr,
        option: Option<RunProgramOption>,
    ) -> Response {
        let max_cost = option.as_ref().and_then(|o| o.max_cost).unwrap_or(0);
        let new_operators = option.as_ref().map(|o| o.new_operators).unwrap_or_default();

        run_program_with_pre_eval(
            allocator,
            &ChiaDialect::new(
                NO_UNKNOWN_OPS | ((new_operators as u32) * ENABLE_BLS_OPS_OUTSIDE_GUARD),
            ),
            program,
            args,
            max_cost,
            option.and_then(|o| o.pre_eval_f),
        )
    }
}
