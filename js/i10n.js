"use strict";

(function() {
  var module = angular.module("angular_i10n", []);

  module.service("L10NService", [function() {
    this.DEFAULT_LOCALE = 'en-US';
    this.prevLocale = this.DEFAULT_LOCALE;
    this.currentLocale = this.DEFAULT_LOCALE;

    this.setLocale = function(locale) {
      this.currentLocale = locale;
      this.prevLocale = locale;
    };

    this.setLocaleTemp = function(locale) {
      this.prevLocale = this.currentLocale;
      this.currentLocale = locale;
    };

    this.revertLocale = function() {
      this.currentLocale = this.prevLocale;
    };

    // Use this method when you're translating variables.
    this.translate = function(txt) {
      return window.i10n[this.currentLocale][txt] || txt;
    };

    // Use this when you're translating a string literal.
    this._ = this.translate;

    module.directive("l10n", ["$rootScope", "L10NService", function() {
      var cleanup;

      return {
        restrict: "EAC",
        link: function(scope, element, attrs) {
          var original = element.text();
          element.text(L10NService.translate(original));
          cleanup = $rootScope.$on("locale-changed", function(locale) {
            element.text(L10NService.translate(original));
          });

          scope.$on("$destroy", function() { cleanup(); });
        }
      };
    }]);

    /*
    // You should really never ever use this unless there is a damn good
    // reason. Filters are called too often. That means the performance of the
    // app will be really really bad.
    // Disabled for now.
    module.filter("l10nf", ["L10NService", function() {
      return function(txt) {
        return L10NService.translate(txt);
      };
    }]);
    */

  }]);

})();