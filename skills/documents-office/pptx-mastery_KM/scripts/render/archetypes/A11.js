module.exports = function createA11Handler(renderers) {
  return function handleA11(ctx) {
    return renderers.renderA11QuadrantMatrix(ctx);
  };
};
