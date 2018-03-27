/// <reference path="types.ts"/>
/** @module todos */
// Auto-generated, edits will be overwritten
import * as gateway from './gateway'

/**
 * @param {object} options Optional options
 * @param {string} [options.id] 
 * @param {string} [options.done] 
 * @param {string} [options.task] 
 * @param {string} [options.due] 
 * @param {string} [options.select] Filtering Columns
 * @param {string} [options.order] Ordering
 * @param {string} [options.Range] Limiting and Pagination
 * @param {string} [options.RangeUnit=items] Limiting and Pagination
 * @param {string} [options.offset] Limiting and Pagination
 * @param {string} [options.limit] Limiting and Pagination
 * @param {string} [options.Prefer] Enum: count=none. Preference
 * @return {Promise<module:types.todos>} OK
 */
export function getTodos(options?: GetTodosOptions): Promise<api.Response<api.todos>> {
  if (!options) options = {}
  const parameters: api.OperationParamGroups = {
    query: {
      id: options.id,
      done: options.done,
      task: options.task,
      due: options.due,
      select: options.select,
      order: options.order,
      offset: options.offset,
      limit: options.limit
    },
    header: {
      Range: options.Range,
      'Range-Unit': options.RangeUnit,
      Prefer: options.Prefer
    }
  }
  return gateway.request(getTodosOperation, parameters)
}

/**
 * @param {object} options Optional options
 * @param {module:types.todos} [options.todos] todos
 * @param {string} [options.Prefer] Enum: return=representation, return=minimal, return=none. Preference
 * @return {Promise<object>} Created
 */
export function postTodos(options?: PostTodosOptions): Promise<api.Response<any>> {
  if (!options) options = {}
  const parameters: api.OperationParamGroups = {
    body: {
      todos: options.todos
    },
    header: {
      Prefer: options.Prefer
    }
  }
  return gateway.request(postTodosOperation, parameters)
}

/**
 * @param {object} options Optional options
 * @param {string} [options.id] 
 * @param {string} [options.done] 
 * @param {string} [options.task] 
 * @param {string} [options.due] 
 * @param {string} [options.Prefer] Enum: return=representation, return=minimal, return=none. Preference
 * @return {Promise<object>} No Content
 */
export function deleteTodos(options?: DeleteTodosOptions): Promise<api.Response<any>> {
  if (!options) options = {}
  const parameters: api.OperationParamGroups = {
    query: {
      id: options.id,
      done: options.done,
      task: options.task,
      due: options.due
    },
    header: {
      Prefer: options.Prefer
    }
  }
  return gateway.request(deleteTodosOperation, parameters)
}

/**
 * @param {object} options Optional options
 * @param {string} [options.id] 
 * @param {string} [options.done] 
 * @param {string} [options.task] 
 * @param {string} [options.due] 
 * @param {module:types.todos} [options.todos] todos
 * @param {string} [options.Prefer] Enum: return=representation, return=minimal, return=none. Preference
 * @return {Promise<object>} No Content
 */
export function patchTodos(options?: PatchTodosOptions): Promise<api.Response<any>> {
  if (!options) options = {}
  const parameters: api.OperationParamGroups = {
    query: {
      id: options.id,
      done: options.done,
      task: options.task,
      due: options.due
    },
    body: {
      todos: options.todos
    },
    header: {
      Prefer: options.Prefer
    }
  }
  return gateway.request(patchTodosOperation, parameters)
}

export interface GetTodosOptions {
  id?: string
  done?: string
  task?: string
  due?: string
  /**
   * Filtering Columns
   */
  select?: string
  /**
   * Ordering
   */
  order?: string
  /**
   * Limiting and Pagination
   */
  Range?: string
  /**
   * Limiting and Pagination
   */
  RangeUnit?: string
  /**
   * Limiting and Pagination
   */
  offset?: string
  /**
   * Limiting and Pagination
   */
  limit?: string
  /**
   * Preference
   */
  Prefer?: 'count=none'
}

export interface PostTodosOptions {
  /**
   * todos
   */
  todos?: api.todos
  /**
   * Preference
   */
  Prefer?: 'return=representation'|'return=minimal'|'return=none'
}

export interface DeleteTodosOptions {
  id?: string
  done?: string
  task?: string
  due?: string
  /**
   * Preference
   */
  Prefer?: 'return=representation'|'return=minimal'|'return=none'
}

export interface PatchTodosOptions {
  id?: string
  done?: string
  task?: string
  due?: string
  /**
   * todos
   */
  todos?: api.todos
  /**
   * Preference
   */
  Prefer?: 'return=representation'|'return=minimal'|'return=none'
}

const getTodosOperation: api.OperationInfo = {
  path: '/todos',
  method: 'get'
}

const postTodosOperation: api.OperationInfo = {
  path: '/todos',
  contentTypes: ['application/json','application/vnd.pgrst.object+json','text/csv'],
  method: 'post'
}

const deleteTodosOperation: api.OperationInfo = {
  path: '/todos',
  method: 'delete'
}

const patchTodosOperation: api.OperationInfo = {
  path: '/todos',
  contentTypes: ['application/json','application/vnd.pgrst.object+json','text/csv'],
  method: 'patch'
}
