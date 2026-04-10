module.exports = function createA15Handler(renderers) {
  return function handleA15(ctx) {
    return renderers.renderA15CycleLoop(ctx);
  };
};
