app.controller('signupController', ['$scope', '$rootScope', '$state', 'AUTH_EVENTS', 'AuthService', 
  function ($scope, $rootScope, $state, AUTH_EVENTS, AuthService) {
  $scope.credentials = {
    email: '',
    password: ''
  };

  $scope.signup = function (credentials) {
    AuthService.signup(credentials).then(function (user) {
      console.log(user);
      $rootScope.$broadcast(AUTH_EVENTS.signupSuccess);
      // $scope.setCurrentUser(user);
      // $state.go('home')
    }, function () {
      $rootScope.$broadcast(AUTH_EVENTS.signupFailed);
    });
  }; 
}])