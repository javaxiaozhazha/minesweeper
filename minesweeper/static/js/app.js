'use strict'

/* App Module*/
var app = angular.module('minesweeper', [
  'gameControllers',
  'gameServices',
]);

app.directive('ngRightClick', function($parse) {
    return function(scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function(event) {
            scope.$apply(function() {
                event.preventDefault();
                fn(scope, {$event:event});
            });
        });
    };
});

/*Controllers*/
var gameControllers = angular.module('gameControllers', []);

gameControllers.controller('minesweep', ['$scope', '$http', 'gameApiService',
  function($scope, $http, gameApiService){
    $scope.finish = 0;
    $scope.flag = false;
    $scope.init = function(){
      gameApiService.init().success(function(data){
        $scope.board = data;
        $scope.finish = 0;
      });
    };

    $scope.update = function(row, col){
      gameApiService.update(row, col).success(function(data){
        $scope.board = data[0];
        $scope.finish = data[1];
      });
    };

    $scope.flag = function(row, col) {
      gameApiService.flag(row, col).success(function(data){
        $scope.board = data[0];
        $scope.finish = data[1];
      });
    };
  }
]);

/*Services*/
var gameServices = angular.module('gameServices', []);
gameServices.factory('gameApiService', ['$http',
  function($http){
    var urlBase="/api";
    var gameApiService = {};

    gameApiService.init = function(){
      return $http.get(urlBase + '/init');
    }

    gameApiService.update = function(row, col){
      return $http.post(urlBase + '/update', {'row':row, 'col':col});
    }

    return gameApiService;
  }
]);

/*Utility functions*/
