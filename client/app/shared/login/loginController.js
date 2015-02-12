app.controller('loginController', ['$scope', '$rootScope', '$state', 'AUTH_EVENTS', 'AuthService', 
  function ($scope, $rootScope, $state, AUTH_EVENTS, AuthService) {
  $scope.credentials = {
    email: '',
    password: ''
  };

  $scope.login = function (credentials) {
    AuthService.login(credentials).then(function (user) {
      $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
      $scope.setCurrentUser(user);
      $state.go('home')
    }, function () {
      $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
    });
  }; 
}])