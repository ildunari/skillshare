module.exports = function createA23Handler(renderers) {
  return function handleA23(ctx) {
    return renderers.renderA23TeamProfiles(ctx);
  };
};
