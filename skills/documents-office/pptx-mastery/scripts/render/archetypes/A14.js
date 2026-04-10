module.exports = function createA14Handler(renderers) {
  return function handleA14(ctx) {
    return renderers.renderA14ProcessFlow(ctx);
  };
};
