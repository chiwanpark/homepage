(function () {
  'use strict';

  var internalLinks = [
    '127.0.0.1',
    'localhost',
    'chiwanpark.com',
    'chiwanpark-status.azurewebsites.net'
  ];

  var checkInternalLink = function(link) {
    for (var i = 0, length = internalLinks.length; i < length; ++i) {
      if (link === internalLinks[i]) {
        return true;
      }
    }

    return false;
  };

  var fixExternalLink = function () {
    var links = document.links;
    for (var i = 0, length = links.length; i < length; ++i) {
      if (!checkInternalLink(links[i].hostname)) {
        links[i].target = '_blank';
      }
    }
  };

  window.addEventListener('load', fixExternalLink, false);
})();
