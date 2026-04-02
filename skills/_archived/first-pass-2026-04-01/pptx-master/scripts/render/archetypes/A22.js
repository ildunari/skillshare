module.exports = function createA22Handler(renderers) {
  return function handleA22(ctx) {
    return renderers.renderA22Quote(ctx);
  };
};
