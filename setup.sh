export AUTH0_DOMAIN="fsnd-wafa.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone"

export DATABASE_URL="postgres://{}:{}@{}/{}".format('postgres','wafa','localhost:5432','capstone')
export FLASK_APP=app
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=debug