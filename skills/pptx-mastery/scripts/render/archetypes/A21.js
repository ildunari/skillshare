module.exports = function createA21Handler(renderers) {
  return function handleA21(ctx) {
    return renderers.renderA21CaseStudy(ctx);
  };
};
