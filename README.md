# Autocode generation for Redux

a python script which automatically spits out boiler plate redux code for an API call. The output format pertains to the code base @ wishbook.io

Use sagaHelper.py to generate code for action creator, reducer, saga and repo

Usage: `sagaHelper.py ACTION_NAME_ONE ACTION_NAME_TWO …`

```
Now generating helpers with ACTION_ONE, ACTION_TWO




============ACTIONS============
export const ACTION_ONE_ACTION = 'ACTION_ONE_ACTION';
export const ACTION_ONE_SUCCESS = 'ACTION_ONE_SUCCESS';

export const ACTION_TWO_ACTION = 'ACTION_TWO_ACTION';
export const ACTION_TWO_SUCCESS = 'ACTION_TWO_SUCCESS';

export const actionOneAction = (params) => ({
  type: ACTION_ONE_ACTION,
  params,
});

export const actionOneSuccess = (responseActionOne) => ({
  type: ACTION_ONE_SUCCESS,
  responseActionOne,
});

export const actionTwoAction = (params) => ({
  type: ACTION_TWO_ACTION,
  params,
});

export const actionTwoSuccess = (responseActionTwo) => ({
  type: ACTION_TWO_SUCCESS,
  responseActionTwo,
});



============REDUCERS============
  ACTION_ONE_ACTION, ACTION_ONE_SUCCESS,
  ACTION_TWO_ACTION, ACTION_TWO_SUCCESS,

	case ACTION_ONE_ACTION:
	return {
  	...state,
	}
	case ACTION_ONE_SUCCESS:
	return {
  	...state,
  	responseActionOne: action.responseActionOne
	}

	case ACTION_TWO_ACTION:
	return {
  	...state,
	}
	case ACTION_TWO_SUCCESS:
	return {
  	...state,
  	responseActionTwo: action.responseActionTwo
	}



============SAGA============
  ACTION_ONE_ACTION, actionOneSuccess,
  ACTION_TWO_ACTION, actionTwoSuccess,

export function* actionOne(action) {
  try {
    
	if (response) {
  	yield put(actionOneSuccess(response));
	} else {
  	yield put(errorActionSet(error));
	}
  } catch (error) {
	yield put(errorActionSet(error));
  }
}

export function* actionTwo(action) {
  try {
    
	if (response) {
  	yield put(actionTwoSuccess(response));
	} else {
  	yield put(errorActionSet(error));
	}
  } catch (error) {
	yield put(errorActionSet(error));
  }
}

  takeEvery(ACTION_ONE_ACTION, actionOne),
  takeEvery(ACTION_TWO_ACTION, actionTwo),

  actionOne = (params = {}) => {
	const queryParams = {
  	...params
	}
	return this.resource.list(queryParams, false);
  }

  actionTwo = (params = {}) => {
	const queryParams = {
  	...params
	}
	return this.resource.list(queryParams, false);
  }
```
