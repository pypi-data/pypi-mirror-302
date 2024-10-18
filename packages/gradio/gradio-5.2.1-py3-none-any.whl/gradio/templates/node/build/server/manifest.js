const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.CauOI8YG.js","app":"_app/immutable/entry/app.BBs3EG_f.js","imports":["_app/immutable/entry/start.CauOI8YG.js","_app/immutable/chunks/client.ZsAi90yx.js","_app/immutable/entry/app.BBs3EG_f.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-BmCb65-_.js')),
			__memo(() => import('./chunks/1-CZs9dlg4.js')),
			__memo(() => import('./chunks/2-BdI8oWhp.js').then(function (n) { return n.ax; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
