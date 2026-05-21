module.exports = function createA19Handler(renderers) {
  return function handleA19(ctx) {
    return renderers.renderA19TableLight(ctx);
  };
};
