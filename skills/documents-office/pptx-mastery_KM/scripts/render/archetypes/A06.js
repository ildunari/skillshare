module.exports = function createA06Handler(renderers) {
  return function handleA06(ctx) {
    return renderers.renderA6Split3070(ctx);
  };
};
