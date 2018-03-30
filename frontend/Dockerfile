FROM mhart/alpine-node:9 AS prod_build
WORKDIR /app
COPY . /app
RUN npm install
RUN npm run-script build
RUN npm run-script test
RUN rm -rf dist
RUN NODE_ENV=production npm run-script build

FROM mhart/alpine-node:9
WORKDIR /app
COPY --from=prod_build /app/dist /app/dist
COPY --from=prod_build /app/bin/server.js /app
CMD node server.js
