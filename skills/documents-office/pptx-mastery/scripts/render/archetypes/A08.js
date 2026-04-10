module.exports = function createA08Handler(renderers) {
  return function handleA08(ctx) {
    return renderers.renderA8IconGrid(ctx);
  };
};
