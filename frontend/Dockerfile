FROM mhart/alpine-node:9 AS prod_build
WORKDIR /app
COPY . /app
RUN npm install
RUN npm run-script build
RUN npm run-script test
RUN rm -rf dist
RUN NODE_ENV=production npm run-script build

FROM mhart/alpine-node:9
WORKDIR /app/workdir
COPY --from=prod_build /app/dist /app/dist
WORKDIR /app/server
COPY --from=prod_build /app/server/ /app/server
RUN npm install
EXPOSE 3000
CMD node server.js
