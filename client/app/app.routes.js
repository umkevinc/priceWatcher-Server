app.config(['$stateProvider', '$urlRouterProvider', 'USER_ROLES', 
			function($stateProvider, $urlRouterProvider, USER_ROLES){
	$urlRouterProvider.otherwise('/home');

	$stateProvider
		.state('home', {
			url: '/home',
			templateUrl: 'app/components/home/partial-home.html',			
		})
		.state('track', {
			url: '/track',
			templateUrl: 'app/components/trackPrice/partial-track-price.html',
			controller: 'trackController',
		})
		.state('deals', {
			url: '/deals',
			templateUrl: 'app/components/findDeals/partial-find-deals.html',
			//controller: 'dealsController'			
		})
		.state('watchlist', {
			url: '/watchlist',
			templateUrl: 'app/components/watchList/partial-watchlist.html',
			//controller: 'watchlistController'
			data: {
		      authorizedRoles: [USER_ROLES.all]
		    }
		})
		.state('login', {
			url: '/login',
			templateUrl: 'app/shared/login/login-form.html',
			controller: 'loginController',			
		})
		.state('logout', {
			url: '/logout',
			templateUrl: 'app/shared/logout/logout-page.html',			
		})
}]);