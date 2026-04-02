module.exports = function createA13Handler(renderers) {
  return function handleA13(ctx) {
    return renderers.renderA13TimelineVertical(ctx);
  };
};
