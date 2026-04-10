module.exports = function createA12Handler(renderers) {
  return function handleA12(ctx) {
    return renderers.renderA12TimelineHorizontal(ctx);
  };
};
