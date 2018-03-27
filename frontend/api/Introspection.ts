/// <reference path="types.ts"/>
/** @module Introspection */
// Auto-generated, edits will be overwritten
import * as gateway from './gateway'

/**
 * OpenAPI description (this document)
 */
export function get(): Promise<api.Response<any>> {
  return gateway.request(getOperation)
}

const getOperation: api.OperationInfo = {
  path: '/',
  method: 'get'
}
