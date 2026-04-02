module.exports = function createA10Handler(renderers) {
  return function handleA10(ctx) {
    return renderers.renderA10Comparison(ctx);
  };
};
