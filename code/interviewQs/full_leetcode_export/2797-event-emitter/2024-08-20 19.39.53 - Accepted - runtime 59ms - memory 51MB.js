class EventEmitter {
  constructor() {
    this.callbackmap = new Map();
  }

  /**
   * @param {string} eventName
   * @param {Function} callback
   * @return {Object}
   */
  subscribe(eventName, callback) {
    if (!this.callbackmap.has(eventName)) {
      this.callbackmap.set(eventName, [callback]);
    } else {
      const existing_callbacks = this.callbackmap.get(eventName);
      if (!existing_callbacks.includes(callback)) {
        existing_callbacks.push(callback);
      }
    }

    return {
      unsubscribe: () => {
        if (this.callbackmap.has(eventName)) {
          const existing_callbacks = this.callbackmap.get(eventName);
          const idx = existing_callbacks.indexOf(callback);
          if (idx > -1) {
            existing_callbacks.splice(idx, 1);
            if (existing_callbacks.length === 0) {
              this.callbackmap.delete(eventName);
            };
          };
        };
      },
    };
  }

  /**
   * @param {string} eventName
   * @param {Array} args
   * @return {Array}
   */
  emit(eventName, args = []) {
    if (this.callbackmap.has(eventName)) {
      const existing_callbacks = this.callbackmap.get(eventName);

      if (existing_callbacks === null) {
        return [];
      }
      const cb_results = [];
      for (const cb of existing_callbacks) {
        cb_results.push(cb(...args));
      }
      return cb_results;
    } else {
      return [];
    }
  }
}