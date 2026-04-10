module.exports = function createA04Handler(renderers) {
  return function handleA04(ctx) {
    return renderers.renderA4AssertionHeroVisual(ctx);
  };
};
