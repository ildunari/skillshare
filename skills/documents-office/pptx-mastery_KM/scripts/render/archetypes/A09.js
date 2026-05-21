module.exports = function createA09Handler(renderers) {
  return function handleA09(ctx) {
    return renderers.renderA9CardGrid(ctx);
  };
};
