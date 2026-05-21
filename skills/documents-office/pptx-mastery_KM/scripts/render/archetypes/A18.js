module.exports = function createA18Handler(renderers) {
  return function handleA18(ctx) {
    return renderers.renderA18AnnotatedChart(ctx);
  };
};
