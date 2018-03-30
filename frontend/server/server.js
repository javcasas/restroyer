// Run as `node bin/serve_static.js`
// Runs a server on port 3000 for the contents of static/dist
// with cross-site headers and everything
// Perfect for trying a production build on your own box

var express = require('express');
var app = express();
app
.use(express.static('/app/dist'))
.use(require('connect-history-api-fallback')())
.use(function(req, res, next){
    // Fallback: any URL that is not recognised becomes `index.html`
    // so the links to sub-pages are sent to the root page,
    // where the SPA routing will take on and forward to the right section.
    // Without this, the reset password page (among others) becomes unreachable from emails
    // because it returns a 404.
    res.sendFile('index.html', {root: "/app/dist"})
})
.listen(3000);
