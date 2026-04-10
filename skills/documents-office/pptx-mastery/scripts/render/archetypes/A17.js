module.exports = function createA17Handler(renderers) {
  return function handleA17(ctx) {
    return renderers.renderA17ChartFirstInsight(ctx);
  };
};
