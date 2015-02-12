app.factory('AuthService', ['$http', 'Session', function ($http, Session) {
  return {
    login: function (credentials) {
      return $http
        .post('http://localhost:5000/api/v1/sessions', credentials)
        .then(function (res) {
          console.log(res);
          var data = res.data;
          // Fake Data
          data.role = '*';
          data.name = 'Kevin'
          data.userid = data.email;
          console.log(data);
          Session.create(data.id, data.userid, data.role);
          console.log("Session Created!");
          return data
        });
	  },
    signup: function(credentials){      
      return $http
        .post('http://localhost:5000/api/v1/users', credentials)
        .then(function(res){
          console.log(res);
          var data = res.data;                  
          return data
        });
    },
	  isAuthenticated: function () {
      return !!Session.userId;
	  },
    isAuthorized: function (authorizedRoles) {
      if (!angular.isArray(authorizedRoles)) {
        authorizedRoles = [authorizedRoles];
      }
      return this.isAuthenticated() && 
      		 authorizedRoles.indexOf(Session.userRole) !== -1;
    }
  };
}])