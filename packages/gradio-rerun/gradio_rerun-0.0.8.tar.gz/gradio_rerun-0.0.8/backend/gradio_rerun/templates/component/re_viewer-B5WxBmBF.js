function me() {
  const A = {};
  typeof document < "u" && document.currentScript !== null && new URL(document.currentScript.src, location.href).toString();
  let b, s = 0, P = null;
  function T() {
    return (P === null || P.byteLength === 0) && (P = new Uint8Array(b.memory.buffer)), P;
  }
  const M = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : { encode: () => {
    throw Error("TextEncoder not available");
  } }, Q = typeof M.encodeInto == "function" ? function(n, e) {
    return M.encodeInto(n, e);
  } : function(n, e) {
    const t = M.encode(n);
    return e.set(t), {
      read: n.length,
      written: t.length
    };
  };
  function m(n, e, t) {
    if (t === void 0) {
      const f = M.encode(n), w = e(f.length, 1) >>> 0;
      return T().subarray(w, w + f.length).set(f), s = f.length, w;
    }
    let r = n.length, _ = e(r, 1) >>> 0;
    const c = T();
    let o = 0;
    for (; o < r; o++) {
      const f = n.charCodeAt(o);
      if (f > 127) break;
      c[_ + o] = f;
    }
    if (o !== r) {
      o !== 0 && (n = n.slice(o)), _ = t(_, r, r = o + n.length * 3, 1) >>> 0;
      const f = T().subarray(_ + o, _ + r), w = Q(n, f);
      o += w.written, _ = t(_, r, o, 1) >>> 0;
    }
    return s = o, _;
  }
  function g(n) {
    return n == null;
  }
  let I = null;
  function a() {
    return (I === null || I.buffer.detached === !0 || I.buffer.detached === void 0 && I.buffer !== b.memory.buffer) && (I = new DataView(b.memory.buffer)), I;
  }
  const W = typeof TextDecoder < "u" ? new TextDecoder("utf-8", { ignoreBOM: !0, fatal: !0 }) : { decode: () => {
    throw Error("TextDecoder not available");
  } };
  typeof TextDecoder < "u" && W.decode();
  function i(n, e) {
    return n = n >>> 0, W.decode(T().subarray(n, n + e));
  }
  function L(n) {
    const e = typeof n;
    if (e == "number" || e == "boolean" || n == null)
      return `${n}`;
    if (e == "string")
      return `"${n}"`;
    if (e == "symbol") {
      const _ = n.description;
      return _ == null ? "Symbol" : `Symbol(${_})`;
    }
    if (e == "function") {
      const _ = n.name;
      return typeof _ == "string" && _.length > 0 ? `Function(${_})` : "Function";
    }
    if (Array.isArray(n)) {
      const _ = n.length;
      let c = "[";
      _ > 0 && (c += L(n[0]));
      for (let o = 1; o < _; o++)
        c += ", " + L(n[o]);
      return c += "]", c;
    }
    const t = /\[object ([^\]]+)\]/.exec(toString.call(n));
    let r;
    if (t.length > 1)
      r = t[1];
    else
      return toString.call(n);
    if (r == "Object")
      try {
        return "Object(" + JSON.stringify(n) + ")";
      } catch {
        return "Object";
      }
    return n instanceof Error ? `${n.name}: ${n.message}
${n.stack}` : r;
  }
  const E = typeof FinalizationRegistry > "u" ? { register: () => {
  }, unregister: () => {
  } } : new FinalizationRegistry((n) => {
    b == null || b.__wbindgen_export_3.get(n.dtor)(n.a, n.b);
  });
  function x(n, e, t, r) {
    const _ = { a: n, b: e, cnt: 1, dtor: t }, c = (...o) => {
      _.cnt++;
      const f = _.a;
      _.a = 0;
      try {
        return r(f, _.b, ...o);
      } finally {
        --_.cnt === 0 ? (b.__wbindgen_export_3.get(_.dtor)(f, _.b), E.unregister(_)) : _.a = f;
      }
    };
    return c.original = _, E.register(c, _, _), c;
  }
  function R(n) {
    const e = b.__wbindgen_export_2.get(n);
    return b.__externref_table_dealloc(n), e;
  }
  function N(n, e, t) {
    try {
      const c = b.__wbindgen_add_to_stack_pointer(-16);
      b.closure89_externref_shim(c, n, e, t);
      var r = a().getInt32(c + 4 * 0, !0), _ = a().getInt32(c + 4 * 1, !0);
      if (_)
        throw R(r);
    } finally {
      b.__wbindgen_add_to_stack_pointer(16);
    }
  }
  function X(n, e) {
    b._dyn_core__ops__function__FnMut_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__hf109e5c77ef44e01(n, e);
  }
  function Y(n, e) {
    try {
      const _ = b.__wbindgen_add_to_stack_pointer(-16);
      b._dyn_core__ops__function__FnMut_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__he0da33c1926a6213(_, n, e);
      var t = a().getInt32(_ + 4 * 0, !0), r = a().getInt32(_ + 4 * 1, !0);
      if (r)
        throw R(t);
    } finally {
      b.__wbindgen_add_to_stack_pointer(16);
    }
  }
  function z(n, e, t) {
    b.closure5021_externref_shim(n, e, t);
  }
  function $(n, e) {
    b._dyn_core__ops__function__FnMut_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__h357222ea32b046a5(n, e);
  }
  function Z(n, e) {
    b._dyn_core__ops__function__FnMut_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__ha28c5a2c57e79949(n, e);
  }
  function U(n, e, t, r) {
    const _ = { a: n, b: e, cnt: 1, dtor: t }, c = (...o) => {
      _.cnt++;
      try {
        return r(_.a, _.b, ...o);
      } finally {
        --_.cnt === 0 && (b.__wbindgen_export_3.get(_.dtor)(_.a, _.b), _.a = 0, E.unregister(_));
      }
    };
    return c.original = _, E.register(c, _, _), c;
  }
  function V(n, e, t) {
    b.closure7326_externref_shim(n, e, t);
  }
  function G(n, e, t) {
    b.closure8347_externref_shim(n, e, t);
  }
  function C(n, e, t) {
    b.closure11724_externref_shim(n, e, t);
  }
  function J(n, e, t) {
    b.closure14606_externref_shim(n, e, t);
  }
  function ee(n, e, t) {
    b.closure14679_externref_shim(n, e, t);
  }
  function te(n, e, t) {
    b.closure14713_externref_shim(n, e, t);
  }
  function ne(n, e) {
    const t = e(n.length * 1, 1) >>> 0;
    return T().set(n, t / 1), s = n.length, t;
  }
  A.set_email = function(n) {
    const e = m(n, b.__wbindgen_malloc, b.__wbindgen_realloc), t = s;
    b.set_email(e, t);
  };
  function d(n) {
    const e = b.__externref_table_alloc();
    return b.__wbindgen_export_2.set(e, n), e;
  }
  function u(n, e) {
    try {
      return n.apply(this, e);
    } catch (t) {
      const r = d(t);
      b.__wbindgen_exn_store(r);
    }
  }
  let D = null;
  function re() {
    return (D === null || D.byteLength === 0) && (D = new Uint32Array(b.memory.buffer)), D;
  }
  function v(n, e) {
    return n = n >>> 0, re().subarray(n / 4, n / 4 + e);
  }
  function q(n) {
    return () => {
      throw new Error(`${n} is not defined`);
    };
  }
  let k = null;
  function _e() {
    return (k === null || k.byteLength === 0) && (k = new Float32Array(b.memory.buffer)), k;
  }
  function y(n, e) {
    return n = n >>> 0, _e().subarray(n / 4, n / 4 + e);
  }
  let F = null;
  function ce() {
    return (F === null || F.byteLength === 0) && (F = new Int32Array(b.memory.buffer)), F;
  }
  function B(n, e) {
    return n = n >>> 0, ce().subarray(n / 4, n / 4 + e);
  }
  function be(n, e, t, r) {
    b.closure17408_externref_shim(n, e, t, r);
  }
  const oe = typeof FinalizationRegistry > "u" ? { register: () => {
  }, unregister: () => {
  } } : new FinalizationRegistry((n) => b.__wbg_intounderlyingbytesource_free(n >>> 0, 1));
  class ue {
    __destroy_into_raw() {
      const e = this.__wbg_ptr;
      return this.__wbg_ptr = 0, oe.unregister(this), e;
    }
    free() {
      const e = this.__destroy_into_raw();
      b.__wbg_intounderlyingbytesource_free(e, 0);
    }
    /**
    * @returns {string}
    */
    get type() {
      let e, t;
      try {
        const c = b.__wbindgen_add_to_stack_pointer(-16);
        b.intounderlyingbytesource_type(c, this.__wbg_ptr);
        var r = a().getInt32(c + 4 * 0, !0), _ = a().getInt32(c + 4 * 1, !0);
        return e = r, t = _, i(r, _);
      } finally {
        b.__wbindgen_add_to_stack_pointer(16), b.__wbindgen_free(e, t, 1);
      }
    }
    /**
    * @returns {number}
    */
    get autoAllocateChunkSize() {
      return b.intounderlyingbytesource_autoAllocateChunkSize(this.__wbg_ptr) >>> 0;
    }
    /**
    * @param {ReadableByteStreamController} controller
    */
    start(e) {
      b.intounderlyingbytesource_start(this.__wbg_ptr, e);
    }
    /**
    * @param {ReadableByteStreamController} controller
    * @returns {Promise<any>}
    */
    pull(e) {
      return b.intounderlyingbytesource_pull(this.__wbg_ptr, e);
    }
    /**
    */
    cancel() {
      const e = this.__destroy_into_raw();
      b.intounderlyingbytesource_cancel(e);
    }
  }
  A.IntoUnderlyingByteSource = ue;
  const ae = typeof FinalizationRegistry > "u" ? { register: () => {
  }, unregister: () => {
  } } : new FinalizationRegistry((n) => b.__wbg_intounderlyingsink_free(n >>> 0, 1));
  class fe {
    __destroy_into_raw() {
      const e = this.__wbg_ptr;
      return this.__wbg_ptr = 0, ae.unregister(this), e;
    }
    free() {
      const e = this.__destroy_into_raw();
      b.__wbg_intounderlyingsink_free(e, 0);
    }
    /**
    * @param {any} chunk
    * @returns {Promise<any>}
    */
    write(e) {
      return b.intounderlyingsink_write(this.__wbg_ptr, e);
    }
    /**
    * @returns {Promise<any>}
    */
    close() {
      const e = this.__destroy_into_raw();
      return b.intounderlyingsink_close(e);
    }
    /**
    * @param {any} reason
    * @returns {Promise<any>}
    */
    abort(e) {
      const t = this.__destroy_into_raw();
      return b.intounderlyingsink_abort(t, e);
    }
  }
  A.IntoUnderlyingSink = fe;
  const ie = typeof FinalizationRegistry > "u" ? { register: () => {
  }, unregister: () => {
  } } : new FinalizationRegistry((n) => b.__wbg_intounderlyingsource_free(n >>> 0, 1));
  class ge {
    __destroy_into_raw() {
      const e = this.__wbg_ptr;
      return this.__wbg_ptr = 0, ie.unregister(this), e;
    }
    free() {
      const e = this.__destroy_into_raw();
      b.__wbg_intounderlyingsource_free(e, 0);
    }
    /**
    * @param {ReadableStreamDefaultController} controller
    * @returns {Promise<any>}
    */
    pull(e) {
      return b.intounderlyingsource_pull(this.__wbg_ptr, e);
    }
    /**
    */
    cancel() {
      const e = this.__destroy_into_raw();
      b.intounderlyingsource_cancel(e);
    }
  }
  A.IntoUnderlyingSource = ge;
  const j = typeof FinalizationRegistry > "u" ? { register: () => {
  }, unregister: () => {
  } } : new FinalizationRegistry((n) => b.__wbg_webhandle_free(n >>> 0, 1));
  class we {
    __destroy_into_raw() {
      const e = this.__wbg_ptr;
      return this.__wbg_ptr = 0, j.unregister(this), e;
    }
    free() {
      const e = this.__destroy_into_raw();
      b.__wbg_webhandle_free(e, 0);
    }
    /**
    * @param {any} app_options
    */
    constructor(e) {
      try {
        const c = b.__wbindgen_add_to_stack_pointer(-16);
        b.webhandle_new(c, e);
        var t = a().getInt32(c + 4 * 0, !0), r = a().getInt32(c + 4 * 1, !0), _ = a().getInt32(c + 4 * 2, !0);
        if (_)
          throw R(r);
        return this.__wbg_ptr = t >>> 0, j.register(this, this.__wbg_ptr, this), this;
      } finally {
        b.__wbindgen_add_to_stack_pointer(16);
      }
    }
    /**
    * @param {any} canvas
    * @returns {Promise<void>}
    */
    start(e) {
      return b.webhandle_start(this.__wbg_ptr, e);
    }
    /**
    * @param {boolean | undefined} [value]
    */
    toggle_panel_overrides(e) {
      b.webhandle_toggle_panel_overrides(this.__wbg_ptr, g(e) ? 16777215 : e ? 1 : 0);
    }
    /**
    * @param {string} panel
    * @param {string | undefined} [state]
    */
    override_panel_state(e, t) {
      try {
        const f = b.__wbindgen_add_to_stack_pointer(-16), w = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), l = s;
        var r = g(t) ? 0 : m(t, b.__wbindgen_malloc, b.__wbindgen_realloc), _ = s;
        b.webhandle_override_panel_state(f, this.__wbg_ptr, w, l, r, _);
        var c = a().getInt32(f + 4 * 0, !0), o = a().getInt32(f + 4 * 1, !0);
        if (o)
          throw R(c);
      } finally {
        b.__wbindgen_add_to_stack_pointer(16);
      }
    }
    /**
    */
    destroy() {
      b.webhandle_destroy(this.__wbg_ptr);
    }
    /**
    * @returns {boolean}
    */
    has_panicked() {
      return b.webhandle_has_panicked(this.__wbg_ptr) !== 0;
    }
    /**
    * @returns {string | undefined}
    */
    panic_message() {
      try {
        const r = b.__wbindgen_add_to_stack_pointer(-16);
        b.webhandle_panic_message(r, this.__wbg_ptr);
        var e = a().getInt32(r + 4 * 0, !0), t = a().getInt32(r + 4 * 1, !0);
        let _;
        return e !== 0 && (_ = i(e, t).slice(), b.__wbindgen_free(e, t * 1, 1)), _;
      } finally {
        b.__wbindgen_add_to_stack_pointer(16);
      }
    }
    /**
    * @returns {string | undefined}
    */
    panic_callstack() {
      try {
        const r = b.__wbindgen_add_to_stack_pointer(-16);
        b.webhandle_panic_callstack(r, this.__wbg_ptr);
        var e = a().getInt32(r + 4 * 0, !0), t = a().getInt32(r + 4 * 1, !0);
        let _;
        return e !== 0 && (_ = i(e, t).slice(), b.__wbindgen_free(e, t * 1, 1)), _;
      } finally {
        b.__wbindgen_add_to_stack_pointer(16);
      }
    }
    /**
    * Add a new receiver streaming data from the given url.
    *
    * If `follow_if_http` is `true`, and the url is an HTTP source, the viewer will open the stream
    * in `Following` mode rather than `Playing` mode.
    *
    * Websocket streams are always opened in `Following` mode.
    *
    * It is an error to open a channel twice with the same id.
    * @param {string} url
    * @param {boolean | undefined} [follow_if_http]
    */
    add_receiver(e, t) {
      const r = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), _ = s;
      b.webhandle_add_receiver(this.__wbg_ptr, r, _, g(t) ? 16777215 : t ? 1 : 0);
    }
    /**
    * @param {string} url
    */
    remove_receiver(e) {
      const t = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), r = s;
      b.webhandle_remove_receiver(this.__wbg_ptr, t, r);
    }
    /**
    * Open a new channel for streaming data.
    *
    * It is an error to open a channel twice with the same id.
    * @param {string} id
    * @param {string} channel_name
    */
    open_channel(e, t) {
      const r = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), _ = s, c = m(t, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      b.webhandle_open_channel(this.__wbg_ptr, r, _, c, o);
    }
    /**
    * Close an existing channel for streaming data.
    *
    * No-op if the channel is already closed.
    * @param {string} id
    */
    close_channel(e) {
      const t = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), r = s;
      b.webhandle_close_channel(this.__wbg_ptr, t, r);
    }
    /**
    * Add an rrd to the viewer directly from a byte array.
    * @param {string} id
    * @param {Uint8Array} data
    */
    send_rrd_to_channel(e, t) {
      const r = m(e, b.__wbindgen_malloc, b.__wbindgen_realloc), _ = s, c = ne(t, b.__wbindgen_malloc), o = s;
      b.webhandle_send_rrd_to_channel(this.__wbg_ptr, r, _, c, o);
    }
  }
  A.WebHandle = we;
  async function se(n, e) {
    if (typeof Response == "function" && n instanceof Response) {
      if (typeof WebAssembly.instantiateStreaming == "function")
        try {
          return await WebAssembly.instantiateStreaming(n, e);
        } catch (r) {
          if (n.headers.get("Content-Type") != "application/wasm")
            console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n", r);
          else
            throw r;
        }
      const t = await n.arrayBuffer();
      return await WebAssembly.instantiate(t, e);
    } else {
      const t = await WebAssembly.instantiate(n, e);
      return t instanceof WebAssembly.Instance ? { instance: t, module: n } : t;
    }
  }
  function H() {
    const n = {};
    return n.wbg = {}, n.wbg.__wbindgen_cb_drop = function(e) {
      const t = e.original;
      return t.cnt-- == 1 ? (t.a = 0, !0) : !1;
    }, n.wbg.__wbindgen_is_function = function(e) {
      return typeof e == "function";
    }, n.wbg.__wbindgen_string_get = function(e, t) {
      const r = t, _ = typeof r == "string" ? r : void 0;
      var c = g(_) ? 0 : m(_, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      a().setInt32(e + 4 * 1, o, !0), a().setInt32(e + 4 * 0, c, !0);
    }, n.wbg.__wbindgen_boolean_get = function(e) {
      const t = e;
      return typeof t == "boolean" ? t ? 1 : 0 : 2;
    }, n.wbg.__wbindgen_is_string = function(e) {
      return typeof e == "string";
    }, n.wbg.__wbindgen_is_object = function(e) {
      const t = e;
      return typeof t == "object" && t !== null;
    }, n.wbg.__wbindgen_is_undefined = function(e) {
      return e === void 0;
    }, n.wbg.__wbindgen_in = function(e, t) {
      return e in t;
    }, n.wbg.__wbindgen_number_new = function(e) {
      return e;
    }, n.wbg.__wbindgen_is_falsy = function(e) {
      return !e;
    }, n.wbg.__wbindgen_is_null = function(e) {
      return e === null;
    }, n.wbg.__wbindgen_error_new = function(e, t) {
      return new Error(i(e, t));
    }, n.wbg.__wbg_structuredClone_0a2cce08b03a6aa2 = function() {
      return u(function(e) {
        return window.structuredClone(e);
      }, arguments);
    }, n.wbg.__wbindgen_string_new = function(e, t) {
      return i(e, t);
    }, n.wbg.__wbindgen_jsval_loose_eq = function(e, t) {
      return e == t;
    }, n.wbg.__wbindgen_number_get = function(e, t) {
      const r = t, _ = typeof r == "number" ? r : void 0;
      a().setFloat64(e + 8 * 1, g(_) ? 0 : _, !0), a().setInt32(e + 4 * 0, !g(_), !0);
    }, n.wbg.__wbindgen_as_number = function(e) {
      return +e;
    }, n.wbg.__wbg_getwithrefkey_edc2c8960f0f1191 = function(e, t) {
      return e[t];
    }, n.wbg.__wbg_set_f975102236d3c502 = function(e, t, r) {
      e[t] = r;
    }, n.wbg.__wbg_error_ecb8b2ef9f17fff0 = function(e, t) {
      let r, _;
      try {
        r = e, _ = t, console.error(i(e, t));
      } finally {
        b.__wbindgen_free(r, _, 1);
      }
    }, n.wbg.__wbg_new_5a0c9fd4e0a0fcbe = function() {
      return new Error();
    }, n.wbg.__wbg_stack_97b8ae9669382e90 = function(e, t) {
      const r = t.stack, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_new_b66ba1cffb2b0651 = function() {
      return new Error();
    }, n.wbg.__wbg_stack_79d726e85295a40e = function(e, t) {
      const r = t.stack, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_instanceof_GpuAdapter_ba82c448cfa55608 = function(e) {
      let t;
      try {
        t = e instanceof GPUAdapter;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_instanceof_GpuDeviceLostInfo_c7232ceb822b15d6 = function(e) {
      let t;
      try {
        t = e instanceof GPUDeviceLostInfo;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_instanceof_GpuValidationError_05482398d349fd2d = function(e) {
      let t;
      try {
        t = e instanceof GPUValidationError;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_message_4bd9ef09b3092122 = function(e, t) {
      const r = t.message, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_instanceof_GpuOutOfMemoryError_658135cd3b3f08e2 = function(e) {
      let t;
      try {
        t = e instanceof GPUOutOfMemoryError;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_type_c3e79de7c41f03c2 = function(e) {
      const t = e.type;
      return { error: 0, warning: 1, info: 2 }[t] ?? 3;
    }, n.wbg.__wbg_offset_47f9a19926637c8e = function(e) {
      return e.offset;
    }, n.wbg.__wbg_length_ff62902e8840f82f = function(e) {
      return e.length;
    }, n.wbg.__wbg_lineNum_06a4c70c1027df81 = function(e) {
      return e.lineNum;
    }, n.wbg.__wbg_message_0ff806941d54e1d2 = function(e, t) {
      const r = t.message, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_getMappedRange_08e71df297c66a50 = function(e, t, r) {
      return e.getMappedRange(t, r);
    }, n.wbg.__wbg_dispatchWorkgroups_f0fd90dcd4a506fa = function(e, t, r, _) {
      e.dispatchWorkgroups(t >>> 0, r >>> 0, _ >>> 0);
    }, n.wbg.__wbg_dispatchWorkgroupsIndirect_567a84763f6a0b87 = function(e, t, r) {
      e.dispatchWorkgroupsIndirect(t, r);
    }, n.wbg.__wbg_end_bbe499813ce72830 = function(e) {
      e.end();
    }, n.wbg.__wbg_setPipeline_4d0e04e7370f0e2e = function(e, t) {
      e.setPipeline(t);
    }, n.wbg.__wbg_setBindGroup_48300d51a3d74853 = function(e, t, r) {
      e.setBindGroup(t >>> 0, r);
    }, n.wbg.__wbg_setBindGroup_d79f4f1d5e43c06f = function(e, t, r, _, c, o, f) {
      e.setBindGroup(t >>> 0, r, v(_, c), o, f >>> 0);
    }, n.wbg.__wbg_getBindGroupLayout_0194b7a790ac805d = function(e, t) {
      return e.getBindGroupLayout(t >>> 0);
    }, n.wbg.__wbg_reason_436ee862de561851 = function(e) {
      const t = e.reason;
      return { unknown: 0, destroyed: 1 }[t] ?? 2;
    }, n.wbg.__wbg_message_54cb97c0fd1579bf = function(e, t) {
      const r = t.message, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_getCompilationInfo_adcb4d74ed54d1f9 = function(e) {
      return e.getCompilationInfo();
    }, n.wbg.__wbg_features_e7f12cb6c5258238 = function(e) {
      return e.features;
    }, n.wbg.__wbg_limits_622a6ae19a037dbf = function(e) {
      return e.limits;
    }, n.wbg.__wbg_requestDevice_1c8e4f0fe8729328 = function(e, t) {
      return e.requestDevice(t);
    }, n.wbg.__wbg_finish_5be91110098e071c = function(e) {
      return e.finish();
    }, n.wbg.__wbg_finish_667443ed0047f53a = function(e, t) {
      return e.finish(t);
    }, n.wbg.__wbg_setBindGroup_de4812744c6ebb6c = function(e, t, r) {
      e.setBindGroup(t >>> 0, r);
    }, n.wbg.__wbg_setBindGroup_92581920e209bf52 = function(e, t, r, _, c, o, f) {
      e.setBindGroup(t >>> 0, r, v(_, c), o, f >>> 0);
    }, n.wbg.__wbg_draw_29abcb466fee48b4 = function(e, t, r, _, c) {
      e.draw(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_drawIndexed_34b06707991ddaf7 = function(e, t, r, _, c, o) {
      e.drawIndexed(t >>> 0, r >>> 0, _ >>> 0, c, o >>> 0);
    }, n.wbg.__wbg_drawIndexedIndirect_4b7b51fa979657ca = function(e, t, r) {
      e.drawIndexedIndirect(t, r);
    }, n.wbg.__wbg_drawIndirect_0054fe754e8e46e9 = function(e, t, r) {
      e.drawIndirect(t, r);
    }, n.wbg.__wbg_setIndexBuffer_91b6f5eb1a43df9b = function(e, t, r, _) {
      e.setIndexBuffer(t, ["uint16", "uint32"][r], _);
    }, n.wbg.__wbg_setIndexBuffer_5bce79843be8653d = function(e, t, r, _, c) {
      e.setIndexBuffer(t, ["uint16", "uint32"][r], _, c);
    }, n.wbg.__wbg_setPipeline_6174c2e8900fe24a = function(e, t) {
      e.setPipeline(t);
    }, n.wbg.__wbg_setVertexBuffer_d9b48c3489dcfa22 = function(e, t, r, _) {
      e.setVertexBuffer(t >>> 0, r, _);
    }, n.wbg.__wbg_setVertexBuffer_330ab505b9dfc64b = function(e, t, r, _, c) {
      e.setVertexBuffer(t >>> 0, r, _, c);
    }, n.wbg.__wbg_gpu_7d756a02ad45027d = function(e) {
      return e.gpu;
    }, n.wbg.__wbg_createView_87e589e1574ba76c = function(e, t) {
      return e.createView(t);
    }, n.wbg.__wbg_destroy_b040948312c539a9 = function(e) {
      e.destroy();
    }, n.wbg.__wbg_error_520ca6f621497012 = function(e) {
      return e.error;
    }, n.wbg.__wbg_instanceof_GpuCanvasContext_1eacd2a8c6b36ada = function(e) {
      let t;
      try {
        t = e instanceof GPUCanvasContext;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_configure_48cfbf148a9998c2 = function(e, t) {
      e.configure(t);
    }, n.wbg.__wbg_getCurrentTexture_1c8e29bec577927d = function(e) {
      return e.getCurrentTexture();
    }, n.wbg.__wbg_features_b1971639ec1a77f7 = function(e) {
      return e.features;
    }, n.wbg.__wbg_limits_e806d307d42a9dde = function(e) {
      return e.limits;
    }, n.wbg.__wbg_queue_e124eaca54d285d4 = function(e) {
      return e.queue;
    }, n.wbg.__wbg_lost_02e8ddfb37103cc2 = function(e) {
      return e.lost;
    }, n.wbg.__wbg_setonuncapturederror_c702acc9eeeb9613 = function(e, t) {
      e.onuncapturederror = t;
    }, n.wbg.__wbg_createBindGroup_f93afa3a0a06b10e = function(e, t) {
      return e.createBindGroup(t);
    }, n.wbg.__wbg_createBindGroupLayout_4243a95be946d48a = function(e, t) {
      return e.createBindGroupLayout(t);
    }, n.wbg.__wbg_createBuffer_44406243485760b1 = function(e, t) {
      return e.createBuffer(t);
    }, n.wbg.__wbg_createCommandEncoder_c7eddb5143f91992 = function(e, t) {
      return e.createCommandEncoder(t);
    }, n.wbg.__wbg_createComputePipeline_fb60500f9a96e290 = function(e, t) {
      return e.createComputePipeline(t);
    }, n.wbg.__wbg_createPipelineLayout_bcb406883550f9cc = function(e, t) {
      return e.createPipelineLayout(t);
    }, n.wbg.__wbg_createQuerySet_4040f9ea5a2ac03c = function(e, t) {
      return e.createQuerySet(t);
    }, n.wbg.__wbg_createRenderBundleEncoder_d9644450ab4cad8f = function(e, t) {
      return e.createRenderBundleEncoder(t);
    }, n.wbg.__wbg_createRenderPipeline_7ca396c186d8d06a = function(e, t) {
      return e.createRenderPipeline(t);
    }, n.wbg.__wbg_createSampler_ed81ff565caa903a = function(e, t) {
      return e.createSampler(t);
    }, n.wbg.__wbg_createShaderModule_cda89eb5c1073627 = function(e, t) {
      return e.createShaderModule(t);
    }, n.wbg.__wbg_createTexture_06106f81b60e5462 = function(e, t) {
      return e.createTexture(t);
    }, n.wbg.__wbg_destroy_2a8c41712abac4cb = function(e) {
      e.destroy();
    }, n.wbg.__wbg_popErrorScope_6d6b4abc95412374 = function(e) {
      return e.popErrorScope();
    }, n.wbg.__wbg_pushErrorScope_3dc565fa86fee870 = function(e, t) {
      e.pushErrorScope(["validation", "out-of-memory", "internal"][t]);
    }, n.wbg.__wbg_getPreferredCanvasFormat_d55bc32b5a6b948a = function(e) {
      const t = e.getPreferredCanvasFormat();
      return { r8unorm: 0, r8snorm: 1, r8uint: 2, r8sint: 3, r16uint: 4, r16sint: 5, r16float: 6, rg8unorm: 7, rg8snorm: 8, rg8uint: 9, rg8sint: 10, r32uint: 11, r32sint: 12, r32float: 13, rg16uint: 14, rg16sint: 15, rg16float: 16, rgba8unorm: 17, "rgba8unorm-srgb": 18, rgba8snorm: 19, rgba8uint: 20, rgba8sint: 21, bgra8unorm: 22, "bgra8unorm-srgb": 23, rgb9e5ufloat: 24, rgb10a2uint: 25, rgb10a2unorm: 26, rg11b10ufloat: 27, rg32uint: 28, rg32sint: 29, rg32float: 30, rgba16uint: 31, rgba16sint: 32, rgba16float: 33, rgba32uint: 34, rgba32sint: 35, rgba32float: 36, stencil8: 37, depth16unorm: 38, depth24plus: 39, "depth24plus-stencil8": 40, depth32float: 41, "depth32float-stencil8": 42, "bc1-rgba-unorm": 43, "bc1-rgba-unorm-srgb": 44, "bc2-rgba-unorm": 45, "bc2-rgba-unorm-srgb": 46, "bc3-rgba-unorm": 47, "bc3-rgba-unorm-srgb": 48, "bc4-r-unorm": 49, "bc4-r-snorm": 50, "bc5-rg-unorm": 51, "bc5-rg-snorm": 52, "bc6h-rgb-ufloat": 53, "bc6h-rgb-float": 54, "bc7-rgba-unorm": 55, "bc7-rgba-unorm-srgb": 56, "etc2-rgb8unorm": 57, "etc2-rgb8unorm-srgb": 58, "etc2-rgb8a1unorm": 59, "etc2-rgb8a1unorm-srgb": 60, "etc2-rgba8unorm": 61, "etc2-rgba8unorm-srgb": 62, "eac-r11unorm": 63, "eac-r11snorm": 64, "eac-rg11unorm": 65, "eac-rg11snorm": 66, "astc-4x4-unorm": 67, "astc-4x4-unorm-srgb": 68, "astc-5x4-unorm": 69, "astc-5x4-unorm-srgb": 70, "astc-5x5-unorm": 71, "astc-5x5-unorm-srgb": 72, "astc-6x5-unorm": 73, "astc-6x5-unorm-srgb": 74, "astc-6x6-unorm": 75, "astc-6x6-unorm-srgb": 76, "astc-8x5-unorm": 77, "astc-8x5-unorm-srgb": 78, "astc-8x6-unorm": 79, "astc-8x6-unorm-srgb": 80, "astc-8x8-unorm": 81, "astc-8x8-unorm-srgb": 82, "astc-10x5-unorm": 83, "astc-10x5-unorm-srgb": 84, "astc-10x6-unorm": 85, "astc-10x6-unorm-srgb": 86, "astc-10x8-unorm": 87, "astc-10x8-unorm-srgb": 88, "astc-10x10-unorm": 89, "astc-10x10-unorm-srgb": 90, "astc-12x10-unorm": 91, "astc-12x10-unorm-srgb": 92, "astc-12x12-unorm": 93, "astc-12x12-unorm-srgb": 94 }[t] ?? 95;
    }, n.wbg.__wbg_requestAdapter_8413757c51a35b1d = function(e, t) {
      return e.requestAdapter(t);
    }, n.wbg.__wbg_size_61d4fa05868b79cd = function(e) {
      return e.size;
    }, n.wbg.__wbg_usage_5043ac06189fbe53 = function(e) {
      return e.usage;
    }, n.wbg.__wbg_destroy_387cb19081689594 = function(e) {
      e.destroy();
    }, n.wbg.__wbg_mapAsync_98ce4986e2f6d4af = function(e, t, r, _) {
      return e.mapAsync(t >>> 0, r, _);
    }, n.wbg.__wbg_unmap_efca7885e5daff78 = function(e) {
      e.unmap();
    }, n.wbg.__wbg_messages_6833dfd0ae6a0a7c = function(e) {
      return e.messages;
    }, n.wbg.__wbg_getBindGroupLayout_1490d5a61f4fd56b = function(e, t) {
      return e.getBindGroupLayout(t >>> 0);
    }, n.wbg.__wbg_copyExternalImageToTexture_e192d56d70996ad4 = function(e, t, r, _) {
      e.copyExternalImageToTexture(t, r, _);
    }, n.wbg.__wbg_submit_4283b63806c5d15e = function(e, t) {
      e.submit(t);
    }, n.wbg.__wbg_writeBuffer_6ce87bc6ff22a2b5 = function(e, t, r, _, c, o) {
      e.writeBuffer(t, r, _, c, o);
    }, n.wbg.__wbg_writeTexture_3708ced0dd386721 = function(e, t, r, _, c) {
      e.writeTexture(t, r, _, c);
    }, n.wbg.__wbg_label_81cb6c4ebcba5f4d = function(e, t) {
      const r = t.label, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_beginComputePass_df50d9ddd5f32a63 = function(e, t) {
      return e.beginComputePass(t);
    }, n.wbg.__wbg_beginRenderPass_14284a54cee2063b = function(e, t) {
      return e.beginRenderPass(t);
    }, n.wbg.__wbg_clearBuffer_a5ccb106665ad51e = function(e, t, r) {
      e.clearBuffer(t, r);
    }, n.wbg.__wbg_clearBuffer_f06a69a0aa134d24 = function(e, t, r, _) {
      e.clearBuffer(t, r, _);
    }, n.wbg.__wbg_copyBufferToBuffer_f0736fef84f76be5 = function(e, t, r, _, c, o) {
      e.copyBufferToBuffer(t, r, _, c, o);
    }, n.wbg.__wbg_copyBufferToTexture_aedde01ad3786b4f = function(e, t, r, _) {
      e.copyBufferToTexture(t, r, _);
    }, n.wbg.__wbg_copyTextureToBuffer_268207d3e09dfa81 = function(e, t, r, _) {
      e.copyTextureToBuffer(t, r, _);
    }, n.wbg.__wbg_copyTextureToTexture_7ea3d6de0a82ce7f = function(e, t, r, _) {
      e.copyTextureToTexture(t, r, _);
    }, n.wbg.__wbg_finish_7ad9d3e23124bbc6 = function(e) {
      return e.finish();
    }, n.wbg.__wbg_finish_78696a2f194fbb7a = function(e, t) {
      return e.finish(t);
    }, n.wbg.__wbg_resolveQuerySet_7354946ea63dacbb = function(e, t, r, _, c, o) {
      e.resolveQuerySet(t, r >>> 0, _ >>> 0, c, o >>> 0);
    }, n.wbg.__wbg_has_14b751afdcf0a341 = function(e, t, r) {
      return e.has(i(t, r));
    }, n.wbg.__wbg_maxTextureDimension1D_71c238385d79f287 = function(e) {
      return e.maxTextureDimension1D;
    }, n.wbg.__wbg_maxTextureDimension2D_ce910a0ea6c7213b = function(e) {
      return e.maxTextureDimension2D;
    }, n.wbg.__wbg_maxTextureDimension3D_76032d2a97af63ac = function(e) {
      return e.maxTextureDimension3D;
    }, n.wbg.__wbg_maxTextureArrayLayers_b561668f7e1ebacc = function(e) {
      return e.maxTextureArrayLayers;
    }, n.wbg.__wbg_maxBindGroups_d2b688642140a1bb = function(e) {
      return e.maxBindGroups;
    }, n.wbg.__wbg_maxBindingsPerBindGroup_a3e9e404dd893c83 = function(e) {
      return e.maxBindingsPerBindGroup;
    }, n.wbg.__wbg_maxDynamicUniformBuffersPerPipelineLayout_98a8fbca367148bf = function(e) {
      return e.maxDynamicUniformBuffersPerPipelineLayout;
    }, n.wbg.__wbg_maxDynamicStorageBuffersPerPipelineLayout_0dec6aea74b472ad = function(e) {
      return e.maxDynamicStorageBuffersPerPipelineLayout;
    }, n.wbg.__wbg_maxSampledTexturesPerShaderStage_7a0712465c0a12b4 = function(e) {
      return e.maxSampledTexturesPerShaderStage;
    }, n.wbg.__wbg_maxSamplersPerShaderStage_6716e9792fc2a833 = function(e) {
      return e.maxSamplersPerShaderStage;
    }, n.wbg.__wbg_maxStorageBuffersPerShaderStage_640d34738978a4ff = function(e) {
      return e.maxStorageBuffersPerShaderStage;
    }, n.wbg.__wbg_maxStorageTexturesPerShaderStage_6614a1e40f7e2827 = function(e) {
      return e.maxStorageTexturesPerShaderStage;
    }, n.wbg.__wbg_maxUniformBuffersPerShaderStage_1ff2f3c6468374ae = function(e) {
      return e.maxUniformBuffersPerShaderStage;
    }, n.wbg.__wbg_maxUniformBufferBindingSize_8830a8df4f730637 = function(e) {
      return e.maxUniformBufferBindingSize;
    }, n.wbg.__wbg_maxStorageBufferBindingSize_10b6eb49372335bc = function(e) {
      return e.maxStorageBufferBindingSize;
    }, n.wbg.__wbg_maxVertexBuffers_9f97f2a89863a431 = function(e) {
      return e.maxVertexBuffers;
    }, n.wbg.__wbg_maxBufferSize_1c8b836056558ebf = function(e) {
      return e.maxBufferSize;
    }, n.wbg.__wbg_maxVertexAttributes_cff466bbace9aa7c = function(e) {
      return e.maxVertexAttributes;
    }, n.wbg.__wbg_maxVertexBufferArrayStride_fb650714a5bd0e68 = function(e) {
      return e.maxVertexBufferArrayStride;
    }, n.wbg.__wbg_minUniformBufferOffsetAlignment_0168a0d08b19afbe = function(e) {
      return e.minUniformBufferOffsetAlignment;
    }, n.wbg.__wbg_minStorageBufferOffsetAlignment_3b63a59f37f275f8 = function(e) {
      return e.minStorageBufferOffsetAlignment;
    }, n.wbg.__wbg_maxInterStageShaderComponents_db659eaa3b248a74 = function(e) {
      return e.maxInterStageShaderComponents;
    }, n.wbg.__wbg_maxColorAttachments_e821b856b5cba24e = function(e) {
      return e.maxColorAttachments;
    }, n.wbg.__wbg_maxColorAttachmentBytesPerSample_ab770042dd82a5bf = function(e) {
      return e.maxColorAttachmentBytesPerSample;
    }, n.wbg.__wbg_maxComputeWorkgroupStorageSize_e6773eb1cbfa7a83 = function(e) {
      return e.maxComputeWorkgroupStorageSize;
    }, n.wbg.__wbg_maxComputeInvocationsPerWorkgroup_4ed447998b195973 = function(e) {
      return e.maxComputeInvocationsPerWorkgroup;
    }, n.wbg.__wbg_maxComputeWorkgroupSizeX_de94f4925b26c73c = function(e) {
      return e.maxComputeWorkgroupSizeX;
    }, n.wbg.__wbg_maxComputeWorkgroupSizeY_cb75de6b450c8915 = function(e) {
      return e.maxComputeWorkgroupSizeY;
    }, n.wbg.__wbg_maxComputeWorkgroupSizeZ_6277d18773d70891 = function(e) {
      return e.maxComputeWorkgroupSizeZ;
    }, n.wbg.__wbg_maxComputeWorkgroupsPerDimension_baef21641827881d = function(e) {
      return e.maxComputeWorkgroupsPerDimension;
    }, n.wbg.__wbg_Window_4d1f8d969d639a22 = function(e) {
      return e.Window;
    }, n.wbg.__wbg_WorkerGlobalScope_c4f12290f7d2efed = function(e) {
      return e.WorkerGlobalScope;
    }, n.wbg.__wbg_setPipeline_8f2f5c316ddb7f68 = function(e, t) {
      e.setPipeline(t);
    }, n.wbg.__wbg_setBindGroup_da48569994113ec3 = function(e, t, r) {
      e.setBindGroup(t >>> 0, r);
    }, n.wbg.__wbg_setBindGroup_1c3dd07b998fa943 = function(e, t, r, _, c, o, f) {
      e.setBindGroup(t >>> 0, r, v(_, c), o, f >>> 0);
    }, n.wbg.__wbg_setIndexBuffer_1dc175abfd5d9be9 = function(e, t, r, _) {
      e.setIndexBuffer(t, ["uint16", "uint32"][r], _);
    }, n.wbg.__wbg_setIndexBuffer_a0fcb26f210351b7 = function(e, t, r, _, c) {
      e.setIndexBuffer(t, ["uint16", "uint32"][r], _, c);
    }, n.wbg.__wbg_setVertexBuffer_c347f9618d3f056a = function(e, t, r, _) {
      e.setVertexBuffer(t >>> 0, r, _);
    }, n.wbg.__wbg_setVertexBuffer_40da6368898587db = function(e, t, r, _, c) {
      e.setVertexBuffer(t >>> 0, r, _, c);
    }, n.wbg.__wbg_draw_a3e2be7a25d4af68 = function(e, t, r, _, c) {
      e.draw(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_drawIndexed_f219cccc74b869c5 = function(e, t, r, _, c, o) {
      e.drawIndexed(t >>> 0, r >>> 0, _ >>> 0, c, o >>> 0);
    }, n.wbg.__wbg_drawIndirect_23fc0a72c5f1b993 = function(e, t, r) {
      e.drawIndirect(t, r);
    }, n.wbg.__wbg_drawIndexedIndirect_6839c0505e2eed2e = function(e, t, r) {
      e.drawIndexedIndirect(t, r);
    }, n.wbg.__wbg_setBlendConstant_fd172910ef2cc0c8 = function(e, t) {
      e.setBlendConstant(t);
    }, n.wbg.__wbg_setScissorRect_915b4534e3936f28 = function(e, t, r, _, c) {
      e.setScissorRect(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_setViewport_aff318ede051c64e = function(e, t, r, _, c, o, f) {
      e.setViewport(t, r, _, c, o, f);
    }, n.wbg.__wbg_setStencilReference_e2bb05496423e92e = function(e, t) {
      e.setStencilReference(t >>> 0);
    }, n.wbg.__wbg_executeBundles_0f6b9b3accb5b6a7 = function(e, t) {
      e.executeBundles(t);
    }, n.wbg.__wbg_end_c97b7dbccda72e72 = function(e) {
      e.end();
    }, n.wbg.__wbg_done_2ffa852272310e47 = function(e) {
      return e.done;
    }, n.wbg.__wbg_value_9f6eeb1e2aab8d96 = function(e) {
      return e.value;
    }, n.wbg.__wbg_getReader_ab94afcb5cb7689a = function() {
      return u(function(e) {
        return e.getReader();
      }, arguments);
    }, n.wbg.__wbg_queueMicrotask_481971b0d87f3dd4 = typeof queueMicrotask == "function" ? queueMicrotask : q("queueMicrotask"), n.wbg.__wbg_queueMicrotask_3cbae2ec6b6cd3d6 = function(e) {
      return e.queueMicrotask;
    }, n.wbg.__wbg_instanceof_WebGl2RenderingContext_62ccef896d9204fa = function(e) {
      let t;
      try {
        t = e instanceof WebGL2RenderingContext;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_beginQuery_2babccfce9472da4 = function(e, t, r) {
      e.beginQuery(t >>> 0, r);
    }, n.wbg.__wbg_bindBufferRange_ec55dd1088960c35 = function(e, t, r, _, c, o) {
      e.bindBufferRange(t >>> 0, r >>> 0, _, c, o);
    }, n.wbg.__wbg_bindSampler_f251f0dde3843dc4 = function(e, t, r) {
      e.bindSampler(t >>> 0, r);
    }, n.wbg.__wbg_bindVertexArray_bec56c40e9ec299d = function(e, t) {
      e.bindVertexArray(t);
    }, n.wbg.__wbg_blitFramebuffer_cb1261c0e925d363 = function(e, t, r, _, c, o, f, w, l, p, h) {
      e.blitFramebuffer(t, r, _, c, o, f, w, l, p >>> 0, h >>> 0);
    }, n.wbg.__wbg_bufferData_f552c26392b9837d = function(e, t, r, _) {
      e.bufferData(t >>> 0, r, _ >>> 0);
    }, n.wbg.__wbg_bufferData_94ce174a81b32961 = function(e, t, r, _) {
      e.bufferData(t >>> 0, r, _ >>> 0);
    }, n.wbg.__wbg_bufferSubData_897bff8bd23ca0b4 = function(e, t, r, _) {
      e.bufferSubData(t >>> 0, r, _);
    }, n.wbg.__wbg_clearBufferfv_bd093a58afda7a8b = function(e, t, r, _, c) {
      e.clearBufferfv(t >>> 0, r, y(_, c));
    }, n.wbg.__wbg_clearBufferiv_18ffec9d148aaf4b = function(e, t, r, _, c) {
      e.clearBufferiv(t >>> 0, r, B(_, c));
    }, n.wbg.__wbg_clearBufferuiv_8575fe1b1af9dd15 = function(e, t, r, _, c) {
      e.clearBufferuiv(t >>> 0, r, v(_, c));
    }, n.wbg.__wbg_clientWaitSync_8d3b836729fa705f = function(e, t, r, _) {
      return e.clientWaitSync(t, r >>> 0, _ >>> 0);
    }, n.wbg.__wbg_compressedTexSubImage2D_d2201c663eb7e7c0 = function(e, t, r, _, c, o, f, w, l, p) {
      e.compressedTexSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l, p);
    }, n.wbg.__wbg_compressedTexSubImage2D_088b90b29f544ebc = function(e, t, r, _, c, o, f, w, l) {
      e.compressedTexSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l);
    }, n.wbg.__wbg_compressedTexSubImage3D_8d64b364b8ed6808 = function(e, t, r, _, c, o, f, w, l, p, h, S) {
      e.compressedTexSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h, S);
    }, n.wbg.__wbg_compressedTexSubImage3D_d2b94340686bbb79 = function(e, t, r, _, c, o, f, w, l, p, h) {
      e.compressedTexSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h);
    }, n.wbg.__wbg_copyBufferSubData_026e82b392fb8df2 = function(e, t, r, _, c, o) {
      e.copyBufferSubData(t >>> 0, r >>> 0, _, c, o);
    }, n.wbg.__wbg_copyTexSubImage3D_f2471ef3614db8d4 = function(e, t, r, _, c, o, f, w, l, p) {
      e.copyTexSubImage3D(t >>> 0, r, _, c, o, f, w, l, p);
    }, n.wbg.__wbg_createQuery_88b1a8cbfaeadcd4 = function(e) {
      const t = e.createQuery();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createSampler_ece1b922a455bd52 = function(e) {
      const t = e.createSampler();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createVertexArray_a3e58c38609ae150 = function(e) {
      const t = e.createVertexArray();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_deleteQuery_deba58de1a061092 = function(e, t) {
      e.deleteQuery(t);
    }, n.wbg.__wbg_deleteSampler_341b638a62cece3e = function(e, t) {
      e.deleteSampler(t);
    }, n.wbg.__wbg_deleteSync_ddf848c7dd5cb195 = function(e, t) {
      e.deleteSync(t);
    }, n.wbg.__wbg_deleteVertexArray_81346dd52e54eb57 = function(e, t) {
      e.deleteVertexArray(t);
    }, n.wbg.__wbg_drawArraysInstanced_c375d32782ea8d30 = function(e, t, r, _, c) {
      e.drawArraysInstanced(t >>> 0, r, _, c);
    }, n.wbg.__wbg_drawBuffers_2744e46ab7e02d91 = function(e, t) {
      e.drawBuffers(t);
    }, n.wbg.__wbg_drawElementsInstanced_a416af0d12f00837 = function(e, t, r, _, c, o) {
      e.drawElementsInstanced(t >>> 0, r, _ >>> 0, c, o);
    }, n.wbg.__wbg_endQuery_7e240d815ced0387 = function(e, t) {
      e.endQuery(t >>> 0);
    }, n.wbg.__wbg_fenceSync_0a54247555048537 = function(e, t, r) {
      const _ = e.fenceSync(t >>> 0, r >>> 0);
      return g(_) ? 0 : d(_);
    }, n.wbg.__wbg_framebufferTextureLayer_1b5119ac136418d2 = function(e, t, r, _, c, o) {
      e.framebufferTextureLayer(t >>> 0, r >>> 0, _, c, o);
    }, n.wbg.__wbg_getBufferSubData_5e2bbbbd18f18d52 = function(e, t, r, _) {
      e.getBufferSubData(t >>> 0, r, _);
    }, n.wbg.__wbg_getIndexedParameter_edda23e611d65abb = function() {
      return u(function(e, t, r) {
        return e.getIndexedParameter(t >>> 0, r >>> 0);
      }, arguments);
    }, n.wbg.__wbg_getQueryParameter_ec854b270df79577 = function(e, t, r) {
      return e.getQueryParameter(t, r >>> 0);
    }, n.wbg.__wbg_getSyncParameter_cf9ca45e037f34f4 = function(e, t, r) {
      return e.getSyncParameter(t, r >>> 0);
    }, n.wbg.__wbg_getUniformBlockIndex_8eef3be68190327f = function(e, t, r, _) {
      return e.getUniformBlockIndex(t, i(r, _));
    }, n.wbg.__wbg_invalidateFramebuffer_12eca43686968fe1 = function() {
      return u(function(e, t, r) {
        e.invalidateFramebuffer(t >>> 0, r);
      }, arguments);
    }, n.wbg.__wbg_readBuffer_c6e1ba464c45ded1 = function(e, t) {
      e.readBuffer(t >>> 0);
    }, n.wbg.__wbg_readPixels_f589cb77c7641fb2 = function() {
      return u(function(e, t, r, _, c, o, f, w) {
        e.readPixels(t, r, _, c, o >>> 0, f >>> 0, w);
      }, arguments);
    }, n.wbg.__wbg_readPixels_74eff76a8a707954 = function() {
      return u(function(e, t, r, _, c, o, f, w) {
        e.readPixels(t, r, _, c, o >>> 0, f >>> 0, w);
      }, arguments);
    }, n.wbg.__wbg_renderbufferStorageMultisample_1e0f794803ff8352 = function(e, t, r, _, c, o) {
      e.renderbufferStorageMultisample(t >>> 0, r, _ >>> 0, c, o);
    }, n.wbg.__wbg_samplerParameterf_f58c4ac221503b11 = function(e, t, r, _) {
      e.samplerParameterf(t, r >>> 0, _);
    }, n.wbg.__wbg_samplerParameteri_97baec154acb369e = function(e, t, r, _) {
      e.samplerParameteri(t, r >>> 0, _);
    }, n.wbg.__wbg_texImage2D_75effcb59fe5da7e = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texImage3D_335fce191a5faae5 = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h) {
        e.texImage3D(t >>> 0, r, _, c, o, f, w, l >>> 0, p >>> 0, h);
      }, arguments);
    }, n.wbg.__wbg_texStorage2D_6143bf0d71e869ce = function(e, t, r, _, c, o) {
      e.texStorage2D(t >>> 0, r, _ >>> 0, c, o);
    }, n.wbg.__wbg_texStorage3D_5d6b3c6bfa977000 = function(e, t, r, _, c, o, f) {
      e.texStorage3D(t >>> 0, r, _ >>> 0, c, o, f);
    }, n.wbg.__wbg_texSubImage2D_be0166513e368886 = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage2D_338d11db84a799ed = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage2D_bdc1e6e8b1feae8f = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage2D_edb828ed3708cfdd = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage2D_fbb08177c318e3f2 = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage3D_c571236e8e9908d5 = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h, S) {
        e.texSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h >>> 0, S);
      }, arguments);
    }, n.wbg.__wbg_texSubImage3D_d86e30d5f4ebc0e0 = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h, S) {
        e.texSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h >>> 0, S);
      }, arguments);
    }, n.wbg.__wbg_texSubImage3D_b3526f28e3c2031e = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h, S) {
        e.texSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h >>> 0, S);
      }, arguments);
    }, n.wbg.__wbg_texSubImage3D_7a0f4d63809a0f6e = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h, S) {
        e.texSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h >>> 0, S);
      }, arguments);
    }, n.wbg.__wbg_texSubImage3D_9ee350bf3d5e61ad = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p, h, S) {
        e.texSubImage3D(t >>> 0, r, _, c, o, f, w, l, p >>> 0, h >>> 0, S);
      }, arguments);
    }, n.wbg.__wbg_uniform1ui_010e62706e661170 = function(e, t, r) {
      e.uniform1ui(t, r >>> 0);
    }, n.wbg.__wbg_uniform2fv_83048fbc79c7f362 = function(e, t, r, _) {
      e.uniform2fv(t, y(r, _));
    }, n.wbg.__wbg_uniform2iv_31ff5561a5c51159 = function(e, t, r, _) {
      e.uniform2iv(t, B(r, _));
    }, n.wbg.__wbg_uniform2uiv_4b36f1c57b28c3c6 = function(e, t, r, _) {
      e.uniform2uiv(t, v(r, _));
    }, n.wbg.__wbg_uniform3fv_0ddd3ca056ab3d1f = function(e, t, r, _) {
      e.uniform3fv(t, y(r, _));
    }, n.wbg.__wbg_uniform3iv_eb887b2a339dda97 = function(e, t, r, _) {
      e.uniform3iv(t, B(r, _));
    }, n.wbg.__wbg_uniform3uiv_19cbb50d7afeb7d0 = function(e, t, r, _) {
      e.uniform3uiv(t, v(r, _));
    }, n.wbg.__wbg_uniform4fv_cf977e0dd611bbdd = function(e, t, r, _) {
      e.uniform4fv(t, y(r, _));
    }, n.wbg.__wbg_uniform4iv_b3a606d0b1b87dc9 = function(e, t, r, _) {
      e.uniform4iv(t, B(r, _));
    }, n.wbg.__wbg_uniform4uiv_cb256e285d564825 = function(e, t, r, _) {
      e.uniform4uiv(t, v(r, _));
    }, n.wbg.__wbg_uniformBlockBinding_744b2ad6a5f2cace = function(e, t, r, _) {
      e.uniformBlockBinding(t, r >>> 0, _ >>> 0);
    }, n.wbg.__wbg_uniformMatrix2fv_7e757aaedd0427cf = function(e, t, r, _, c) {
      e.uniformMatrix2fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix2x3fv_91be1a9373d7c5ce = function(e, t, r, _, c) {
      e.uniformMatrix2x3fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix2x4fv_b5ef5b5baced0e4f = function(e, t, r, _, c) {
      e.uniformMatrix2x4fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix3fv_5eec5885a8d5de8b = function(e, t, r, _, c) {
      e.uniformMatrix3fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix3x2fv_88709a0858bab333 = function(e, t, r, _, c) {
      e.uniformMatrix3x2fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix3x4fv_184c4f571cff1122 = function(e, t, r, _, c) {
      e.uniformMatrix3x4fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix4fv_ae100fc474463355 = function(e, t, r, _, c) {
      e.uniformMatrix4fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix4x2fv_e931df9c7cb32d55 = function(e, t, r, _, c) {
      e.uniformMatrix4x2fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix4x3fv_f78c83b4908c3e27 = function(e, t, r, _, c) {
      e.uniformMatrix4x3fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_vertexAttribDivisor_48f4c9ce15c07063 = function(e, t, r) {
      e.vertexAttribDivisor(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_vertexAttribIPointer_78250ec98da971a2 = function(e, t, r, _, c, o) {
      e.vertexAttribIPointer(t >>> 0, r, _ >>> 0, c, o);
    }, n.wbg.__wbg_activeTexture_067b93df6d1ed857 = function(e, t) {
      e.activeTexture(t >>> 0);
    }, n.wbg.__wbg_attachShader_396d529f1d7c9abc = function(e, t, r) {
      e.attachShader(t, r);
    }, n.wbg.__wbg_bindAttribLocation_9e7dad25e51f58b1 = function(e, t, r, _, c) {
      e.bindAttribLocation(t, r >>> 0, i(_, c));
    }, n.wbg.__wbg_bindBuffer_d6b05e0a99a752d4 = function(e, t, r) {
      e.bindBuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindFramebuffer_f5e959313c29a7c6 = function(e, t, r) {
      e.bindFramebuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindRenderbuffer_691cb14fc6248155 = function(e, t, r) {
      e.bindRenderbuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindTexture_840f7fcfd0298dc4 = function(e, t, r) {
      e.bindTexture(t >>> 0, r);
    }, n.wbg.__wbg_blendColor_4c1f00a2e4f1a80d = function(e, t, r, _, c) {
      e.blendColor(t, r, _, c);
    }, n.wbg.__wbg_blendEquation_e7b91e8e062fa502 = function(e, t) {
      e.blendEquation(t >>> 0);
    }, n.wbg.__wbg_blendEquationSeparate_272bfcd932055191 = function(e, t, r) {
      e.blendEquationSeparate(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_blendFunc_6a7b81c06098c023 = function(e, t, r) {
      e.blendFunc(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_blendFuncSeparate_f81dd232d266e735 = function(e, t, r, _, c) {
      e.blendFuncSeparate(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_clear_7a2a7ca897047e8d = function(e, t) {
      e.clear(t >>> 0);
    }, n.wbg.__wbg_clearDepth_a65e67fdeb1f3ff9 = function(e, t) {
      e.clearDepth(t);
    }, n.wbg.__wbg_clearStencil_1f24aec5432f38ba = function(e, t) {
      e.clearStencil(t);
    }, n.wbg.__wbg_colorMask_7c2aafdec5441392 = function(e, t, r, _, c) {
      e.colorMask(t !== 0, r !== 0, _ !== 0, c !== 0);
    }, n.wbg.__wbg_compileShader_77ef81728b1c03f6 = function(e, t) {
      e.compileShader(t);
    }, n.wbg.__wbg_copyTexSubImage2D_d3b3d3b235c88d33 = function(e, t, r, _, c, o, f, w, l) {
      e.copyTexSubImage2D(t >>> 0, r, _, c, o, f, w, l);
    }, n.wbg.__wbg_createBuffer_7b18852edffb3ab4 = function(e) {
      const t = e.createBuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createFramebuffer_a12847edac092647 = function(e) {
      const t = e.createFramebuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createProgram_73611dc7a72c4ee2 = function(e) {
      const t = e.createProgram();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createRenderbuffer_e7bd95fedc0bbcb5 = function(e) {
      const t = e.createRenderbuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createShader_f10ffabbfd8e2c8c = function(e, t) {
      const r = e.createShader(t >>> 0);
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_createTexture_2426b031baa26a82 = function(e) {
      const t = e.createTexture();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_cullFace_fbafcb7763a2d6aa = function(e, t) {
      e.cullFace(t >>> 0);
    }, n.wbg.__wbg_deleteBuffer_27b0fb5ed68afbe4 = function(e, t) {
      e.deleteBuffer(t);
    }, n.wbg.__wbg_deleteFramebuffer_c0d511b2fc07620d = function(e, t) {
      e.deleteFramebuffer(t);
    }, n.wbg.__wbg_deleteProgram_c3238b647d849334 = function(e, t) {
      e.deleteProgram(t);
    }, n.wbg.__wbg_deleteRenderbuffer_325417b497c5ae27 = function(e, t) {
      e.deleteRenderbuffer(t);
    }, n.wbg.__wbg_deleteShader_da06706168cf00dc = function(e, t) {
      e.deleteShader(t);
    }, n.wbg.__wbg_deleteTexture_cdd844345a2559bb = function(e, t) {
      e.deleteTexture(t);
    }, n.wbg.__wbg_depthFunc_2f1df7eb8339f5a3 = function(e, t) {
      e.depthFunc(t >>> 0);
    }, n.wbg.__wbg_depthMask_a301dd9951c6056c = function(e, t) {
      e.depthMask(t !== 0);
    }, n.wbg.__wbg_depthRange_85c249bf5c81856c = function(e, t, r) {
      e.depthRange(t, r);
    }, n.wbg.__wbg_disable_8908871f2334e76b = function(e, t) {
      e.disable(t >>> 0);
    }, n.wbg.__wbg_disableVertexAttribArray_79a5010f18eb84cb = function(e, t) {
      e.disableVertexAttribArray(t >>> 0);
    }, n.wbg.__wbg_drawArrays_7a8f5031b1fe80ff = function(e, t, r, _) {
      e.drawArrays(t >>> 0, r, _);
    }, n.wbg.__wbg_enable_541ed84c1e7d269d = function(e, t) {
      e.enable(t >>> 0);
    }, n.wbg.__wbg_enableVertexAttribArray_06043f51b716ed9d = function(e, t) {
      e.enableVertexAttribArray(t >>> 0);
    }, n.wbg.__wbg_framebufferRenderbuffer_f7c592ad40667f89 = function(e, t, r, _, c) {
      e.framebufferRenderbuffer(t >>> 0, r >>> 0, _ >>> 0, c);
    }, n.wbg.__wbg_framebufferTexture2D_5b524fe6135d5fe8 = function(e, t, r, _, c, o) {
      e.framebufferTexture2D(t >>> 0, r >>> 0, _ >>> 0, c, o);
    }, n.wbg.__wbg_frontFace_54ccf43770ae1011 = function(e, t) {
      e.frontFace(t >>> 0);
    }, n.wbg.__wbg_getExtension_095ef1e6c9d8d8ab = function() {
      return u(function(e, t, r) {
        const _ = e.getExtension(i(t, r));
        return g(_) ? 0 : d(_);
      }, arguments);
    }, n.wbg.__wbg_getParameter_cfaed180705b9280 = function() {
      return u(function(e, t) {
        return e.getParameter(t >>> 0);
      }, arguments);
    }, n.wbg.__wbg_getProgramInfoLog_fe796f3a9512a8e3 = function(e, t, r) {
      const _ = t.getProgramInfoLog(r);
      var c = g(_) ? 0 : m(_, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      a().setInt32(e + 4 * 1, o, !0), a().setInt32(e + 4 * 0, c, !0);
    }, n.wbg.__wbg_getProgramParameter_9df6cbbb1343b27d = function(e, t, r) {
      return e.getProgramParameter(t, r >>> 0);
    }, n.wbg.__wbg_getShaderInfoLog_a7ca51b89a4dafab = function(e, t, r) {
      const _ = t.getShaderInfoLog(r);
      var c = g(_) ? 0 : m(_, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      a().setInt32(e + 4 * 1, o, !0), a().setInt32(e + 4 * 0, c, !0);
    }, n.wbg.__wbg_getShaderParameter_806970126d526c29 = function(e, t, r) {
      return e.getShaderParameter(t, r >>> 0);
    }, n.wbg.__wbg_getSupportedExtensions_e1788ac835b7e81a = function(e) {
      const t = e.getSupportedExtensions();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_getUniformLocation_6a59ad54df3bba8e = function(e, t, r, _) {
      const c = e.getUniformLocation(t, i(r, _));
      return g(c) ? 0 : d(c);
    }, n.wbg.__wbg_linkProgram_56a5d97f63b1f56d = function(e, t) {
      e.linkProgram(t);
    }, n.wbg.__wbg_pixelStorei_3a600280eab03e3c = function(e, t, r) {
      e.pixelStorei(t >>> 0, r);
    }, n.wbg.__wbg_polygonOffset_ebf1b1bd8db53e65 = function(e, t, r) {
      e.polygonOffset(t, r);
    }, n.wbg.__wbg_renderbufferStorage_3c5e469d82dfe89b = function(e, t, r, _, c) {
      e.renderbufferStorage(t >>> 0, r >>> 0, _, c);
    }, n.wbg.__wbg_scissor_2b172ca4e459dd16 = function(e, t, r, _, c) {
      e.scissor(t, r, _, c);
    }, n.wbg.__wbg_shaderSource_b92b2b5c29126344 = function(e, t, r, _) {
      e.shaderSource(t, i(r, _));
    }, n.wbg.__wbg_stencilFuncSeparate_25b5dd967d72b6e5 = function(e, t, r, _, c) {
      e.stencilFuncSeparate(t >>> 0, r >>> 0, _, c >>> 0);
    }, n.wbg.__wbg_stencilMask_702162181d88081f = function(e, t) {
      e.stencilMask(t >>> 0);
    }, n.wbg.__wbg_stencilMaskSeparate_1f803a440e789b81 = function(e, t, r) {
      e.stencilMaskSeparate(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_stencilOpSeparate_52b401966f916a0f = function(e, t, r, _, c) {
      e.stencilOpSeparate(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_texParameteri_531d0268109950ba = function(e, t, r, _) {
      e.texParameteri(t >>> 0, r >>> 0, _);
    }, n.wbg.__wbg_uniform1f_81b570bf6358ae6c = function(e, t, r) {
      e.uniform1f(t, r);
    }, n.wbg.__wbg_uniform1i_ded3be13f5d8f11a = function(e, t, r) {
      e.uniform1i(t, r);
    }, n.wbg.__wbg_uniform4f_bdbb7cf56fc94cbb = function(e, t, r, _, c, o) {
      e.uniform4f(t, r, _, c, o);
    }, n.wbg.__wbg_useProgram_001c6b9208b683d3 = function(e, t) {
      e.useProgram(t);
    }, n.wbg.__wbg_vertexAttribPointer_b435a034ff758637 = function(e, t, r, _, c, o, f) {
      e.vertexAttribPointer(t >>> 0, r, _ >>> 0, c !== 0, o, f);
    }, n.wbg.__wbg_viewport_536c78dd69c44351 = function(e, t, r, _, c) {
      e.viewport(t, r, _, c);
    }, n.wbg.__wbg_instanceof_Window_5012736c80a01584 = function(e) {
      let t;
      try {
        t = e instanceof Window;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_document_8554450897a855b9 = function(e) {
      const t = e.document;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_location_af118da6c50d4c3f = function(e) {
      return e.location;
    }, n.wbg.__wbg_history_489e13d0b625263c = function() {
      return u(function(e) {
        return e.history;
      }, arguments);
    }, n.wbg.__wbg_navigator_6210380287bf8581 = function(e) {
      return e.navigator;
    }, n.wbg.__wbg_devicePixelRatio_7ba8bc80d46340bd = function(e) {
      return e.devicePixelRatio;
    }, n.wbg.__wbg_localStorage_90db5cb66e840248 = function() {
      return u(function(e) {
        const t = e.localStorage;
        return g(t) ? 0 : d(t);
      }, arguments);
    }, n.wbg.__wbg_performance_fa12dc8712926291 = function(e) {
      const t = e.performance;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_isSecureContext_80defc491f0c2d6a = function(e) {
      return e.isSecureContext;
    }, n.wbg.__wbg_getComputedStyle_ba4609b39055f674 = function() {
      return u(function(e, t) {
        const r = e.getComputedStyle(t);
        return g(r) ? 0 : d(r);
      }, arguments);
    }, n.wbg.__wbg_matchMedia_170d35fd154463b2 = function() {
      return u(function(e, t, r) {
        const _ = e.matchMedia(i(t, r));
        return g(_) ? 0 : d(_);
      }, arguments);
    }, n.wbg.__wbg_open_43b3c6577af2a808 = function() {
      return u(function(e, t, r, _, c) {
        const o = e.open(i(t, r), i(_, c));
        return g(o) ? 0 : d(o);
      }, arguments);
    }, n.wbg.__wbg_cancelAnimationFrame_f80ecdad075d1d55 = function() {
      return u(function(e, t) {
        e.cancelAnimationFrame(t);
      }, arguments);
    }, n.wbg.__wbg_requestAnimationFrame_b4b782250b9c2c88 = function() {
      return u(function(e, t) {
        return e.requestAnimationFrame(t);
      }, arguments);
    }, n.wbg.__wbg_clearInterval_df3409c32c572e85 = function(e, t) {
      e.clearInterval(t);
    }, n.wbg.__wbg_fetch_f3adf866d8944b41 = function(e, t) {
      return e.fetch(t);
    }, n.wbg.__wbg_setTimeout_73b734ca971c19f4 = function() {
      return u(function(e, t, r) {
        return e.setTimeout(t, r);
      }, arguments);
    }, n.wbg.__wbg_body_b3bb488e8e54bf4b = function(e) {
      const t = e.body;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_hidden_b3b8c1dc2ee4fc2a = function(e) {
      return e.hidden;
    }, n.wbg.__wbg_activeElement_1036a8ddc10ec3f1 = function(e) {
      const t = e.activeElement;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createElement_5921e9eb06b9ec89 = function() {
      return u(function(e, t, r) {
        return e.createElement(i(t, r));
      }, arguments);
    }, n.wbg.__wbg_getElementById_f56c8e6a15a6926d = function(e, t, r) {
      const _ = e.getElementById(i(t, r));
      return g(_) ? 0 : d(_);
    }, n.wbg.__wbg_querySelector_e21c39150aa72078 = function() {
      return u(function(e, t, r) {
        const _ = e.querySelector(i(t, r));
        return g(_) ? 0 : d(_);
      }, arguments);
    }, n.wbg.__wbg_querySelectorAll_52447cbab6df8bae = function() {
      return u(function(e, t, r) {
        return e.querySelectorAll(i(t, r));
      }, arguments);
    }, n.wbg.__wbg_elementFromPoint_a7b17c0b42d50842 = function(e, t, r) {
      const _ = e.elementFromPoint(t, r);
      return g(_) ? 0 : d(_);
    }, n.wbg.__wbg_instanceof_Element_cc034878d52a64fa = function(e) {
      let t;
      try {
        t = e instanceof Element;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_id_8071f78aa2301217 = function(e, t) {
      const r = t.id, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_setid_b43ed506c9b1e9c5 = function(e, t, r) {
      e.id = i(t, r);
    }, n.wbg.__wbg_setinnerHTML_ea7e3c6a3c4790c6 = function(e, t, r) {
      e.innerHTML = i(t, r);
    }, n.wbg.__wbg_getBoundingClientRect_35fc4d8fa10e0463 = function(e) {
      return e.getBoundingClientRect();
    }, n.wbg.__wbg_setAttribute_d5540a19be09f8dc = function() {
      return u(function(e, t, r, _, c) {
        e.setAttribute(i(t, r), i(_, c));
      }, arguments);
    }, n.wbg.__wbg_remove_5b68b70c39041e2a = function(e) {
      e.remove();
    }, n.wbg.__wbg_instanceof_HtmlElement_ee6cb55e6b90ae79 = function(e) {
      let t;
      try {
        t = e instanceof HTMLElement;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_setinnerText_69255282a5d7ed93 = function(e, t, r) {
      e.innerText = i(t, r);
    }, n.wbg.__wbg_settabIndex_f6fb98fef6cbb39b = function(e, t) {
      e.tabIndex = t;
    }, n.wbg.__wbg_style_e06c9e03355741e9 = function(e) {
      return e.style;
    }, n.wbg.__wbg_offsetTop_3f1fbd1d48327b28 = function(e) {
      return e.offsetTop;
    }, n.wbg.__wbg_setonclick_cdd25d3e6e7636a0 = function(e, t) {
      e.onclick = t;
    }, n.wbg.__wbg_blur_2097e550054a8dc8 = function() {
      return u(function(e) {
        e.blur();
      }, arguments);
    }, n.wbg.__wbg_focus_06621101cc79f5d8 = function() {
      return u(function(e) {
        e.focus();
      }, arguments);
    }, n.wbg.__wbg_framebufferTextureMultiviewOVR_32295d56731dd362 = function(e, t, r, _, c, o, f) {
      e.framebufferTextureMultiviewOVR(t >>> 0, r >>> 0, _, c, o, f);
    }, n.wbg.__wbg_bufferData_fc33089cf05a6c5a = function(e, t, r, _) {
      e.bufferData(t >>> 0, r, _ >>> 0);
    }, n.wbg.__wbg_bufferData_0db2a74470353a96 = function(e, t, r, _) {
      e.bufferData(t >>> 0, r, _ >>> 0);
    }, n.wbg.__wbg_bufferSubData_944883045753ee61 = function(e, t, r, _) {
      e.bufferSubData(t >>> 0, r, _);
    }, n.wbg.__wbg_compressedTexSubImage2D_678be4671393a94b = function(e, t, r, _, c, o, f, w, l) {
      e.compressedTexSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l);
    }, n.wbg.__wbg_readPixels_0c5ad23c72dbe1b8 = function() {
      return u(function(e, t, r, _, c, o, f, w) {
        e.readPixels(t, r, _, c, o >>> 0, f >>> 0, w);
      }, arguments);
    }, n.wbg.__wbg_texImage2D_d704e7eee22d1e6b = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_texSubImage2D_bed4633ee03b384d = function() {
      return u(function(e, t, r, _, c, o, f, w, l, p) {
        e.texSubImage2D(t >>> 0, r, _, c, o, f, w >>> 0, l >>> 0, p);
      }, arguments);
    }, n.wbg.__wbg_uniform2fv_b73144e507d90a92 = function(e, t, r, _) {
      e.uniform2fv(t, y(r, _));
    }, n.wbg.__wbg_uniform2iv_27f3fc3aefa41fa7 = function(e, t, r, _) {
      e.uniform2iv(t, B(r, _));
    }, n.wbg.__wbg_uniform3fv_5df1d945c0bbfe20 = function(e, t, r, _) {
      e.uniform3fv(t, y(r, _));
    }, n.wbg.__wbg_uniform3iv_03be54fcc4468fc4 = function(e, t, r, _) {
      e.uniform3iv(t, B(r, _));
    }, n.wbg.__wbg_uniform4fv_d87e4ea9ef6cf6de = function(e, t, r, _) {
      e.uniform4fv(t, y(r, _));
    }, n.wbg.__wbg_uniform4iv_965df9fa4c8ab47e = function(e, t, r, _) {
      e.uniform4iv(t, B(r, _));
    }, n.wbg.__wbg_uniformMatrix2fv_8646addaa18ba00b = function(e, t, r, _, c) {
      e.uniformMatrix2fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix3fv_917f07d03e8b1db5 = function(e, t, r, _, c) {
      e.uniformMatrix3fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_uniformMatrix4fv_46c1f9033bbb1a5e = function(e, t, r, _, c) {
      e.uniformMatrix4fv(t, r !== 0, y(_, c));
    }, n.wbg.__wbg_activeTexture_b967ed47a8083daa = function(e, t) {
      e.activeTexture(t >>> 0);
    }, n.wbg.__wbg_attachShader_2b5810fc1d23ebe7 = function(e, t, r) {
      e.attachShader(t, r);
    }, n.wbg.__wbg_bindAttribLocation_0018ec2a523f139f = function(e, t, r, _, c) {
      e.bindAttribLocation(t, r >>> 0, i(_, c));
    }, n.wbg.__wbg_bindBuffer_1f581c747176e7d7 = function(e, t, r) {
      e.bindBuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindFramebuffer_8cba9964befd2a6d = function(e, t, r) {
      e.bindFramebuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindRenderbuffer_297ae310683dc32b = function(e, t, r) {
      e.bindRenderbuffer(t >>> 0, r);
    }, n.wbg.__wbg_bindTexture_bffa89324927e23a = function(e, t, r) {
      e.bindTexture(t >>> 0, r);
    }, n.wbg.__wbg_blendColor_c876d94aa784bef7 = function(e, t, r, _, c) {
      e.blendColor(t, r, _, c);
    }, n.wbg.__wbg_blendEquation_4f3b8eb0b07cab21 = function(e, t) {
      e.blendEquation(t >>> 0);
    }, n.wbg.__wbg_blendEquationSeparate_95241ffd0f6ab09e = function(e, t, r) {
      e.blendEquationSeparate(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_blendFunc_f31d0f0d227137e0 = function(e, t, r) {
      e.blendFunc(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_blendFuncSeparate_2b607032f14b9381 = function(e, t, r, _, c) {
      e.blendFuncSeparate(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_clear_780c4e5384fe3fc6 = function(e, t) {
      e.clear(t >>> 0);
    }, n.wbg.__wbg_clearDepth_92f7c7d02e50df24 = function(e, t) {
      e.clearDepth(t);
    }, n.wbg.__wbg_clearStencil_78b0b3c82001b542 = function(e, t) {
      e.clearStencil(t);
    }, n.wbg.__wbg_colorMask_6a64eb75df60e2cf = function(e, t, r, _, c) {
      e.colorMask(t !== 0, r !== 0, _ !== 0, c !== 0);
    }, n.wbg.__wbg_compileShader_043cc8b99c2efc21 = function(e, t) {
      e.compileShader(t);
    }, n.wbg.__wbg_copyTexSubImage2D_8f6644e7df89a307 = function(e, t, r, _, c, o, f, w, l) {
      e.copyTexSubImage2D(t >>> 0, r, _, c, o, f, w, l);
    }, n.wbg.__wbg_createBuffer_9571c039ba6696c6 = function(e) {
      const t = e.createBuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createFramebuffer_20f79ec189ef2060 = function(e) {
      const t = e.createFramebuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createProgram_2c3a8969b5a76988 = function(e) {
      const t = e.createProgram();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createRenderbuffer_620bdfb7867926e8 = function(e) {
      const t = e.createRenderbuffer();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_createShader_af087106532661d9 = function(e, t) {
      const r = e.createShader(t >>> 0);
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_createTexture_e49c36c5f31925a3 = function(e) {
      const t = e.createTexture();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_cullFace_ccad99c645b704eb = function(e, t) {
      e.cullFace(t >>> 0);
    }, n.wbg.__wbg_deleteBuffer_898974b9db136e43 = function(e, t) {
      e.deleteBuffer(t);
    }, n.wbg.__wbg_deleteFramebuffer_d632dfba2c1f5c75 = function(e, t) {
      e.deleteFramebuffer(t);
    }, n.wbg.__wbg_deleteProgram_5f938b0667141206 = function(e, t) {
      e.deleteProgram(t);
    }, n.wbg.__wbg_deleteRenderbuffer_ccae7372581ae424 = function(e, t) {
      e.deleteRenderbuffer(t);
    }, n.wbg.__wbg_deleteShader_b9bb71cfb1a65a0d = function(e, t) {
      e.deleteShader(t);
    }, n.wbg.__wbg_deleteTexture_558c751a66bd2f16 = function(e, t) {
      e.deleteTexture(t);
    }, n.wbg.__wbg_depthFunc_5398fbc3f56db827 = function(e, t) {
      e.depthFunc(t >>> 0);
    }, n.wbg.__wbg_depthMask_9b58af067c6393e9 = function(e, t) {
      e.depthMask(t !== 0);
    }, n.wbg.__wbg_depthRange_29f0e12388f0eacb = function(e, t, r) {
      e.depthRange(t, r);
    }, n.wbg.__wbg_disable_d73e59fee5b5e973 = function(e, t) {
      e.disable(t >>> 0);
    }, n.wbg.__wbg_disableVertexAttribArray_b9d8ae826c70526f = function(e, t) {
      e.disableVertexAttribArray(t >>> 0);
    }, n.wbg.__wbg_drawArrays_532f4e0a4547dd1f = function(e, t, r, _) {
      e.drawArrays(t >>> 0, r, _);
    }, n.wbg.__wbg_enable_68b3fa03a633259a = function(e, t) {
      e.enable(t >>> 0);
    }, n.wbg.__wbg_enableVertexAttribArray_52c23a516be565c0 = function(e, t) {
      e.enableVertexAttribArray(t >>> 0);
    }, n.wbg.__wbg_framebufferRenderbuffer_fee6ceb2330389b7 = function(e, t, r, _, c) {
      e.framebufferRenderbuffer(t >>> 0, r >>> 0, _ >>> 0, c);
    }, n.wbg.__wbg_framebufferTexture2D_ae81a33228e46de6 = function(e, t, r, _, c, o) {
      e.framebufferTexture2D(t >>> 0, r >>> 0, _ >>> 0, c, o);
    }, n.wbg.__wbg_frontFace_358bf8c6c5159d54 = function(e, t) {
      e.frontFace(t >>> 0);
    }, n.wbg.__wbg_getParameter_8df84a84197f2148 = function() {
      return u(function(e, t) {
        return e.getParameter(t >>> 0);
      }, arguments);
    }, n.wbg.__wbg_getProgramInfoLog_22296c36addf7a70 = function(e, t, r) {
      const _ = t.getProgramInfoLog(r);
      var c = g(_) ? 0 : m(_, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      a().setInt32(e + 4 * 1, o, !0), a().setInt32(e + 4 * 0, c, !0);
    }, n.wbg.__wbg_getProgramParameter_ab2954ca517d8589 = function(e, t, r) {
      return e.getProgramParameter(t, r >>> 0);
    }, n.wbg.__wbg_getShaderInfoLog_935361c52a919c15 = function(e, t, r) {
      const _ = t.getShaderInfoLog(r);
      var c = g(_) ? 0 : m(_, b.__wbindgen_malloc, b.__wbindgen_realloc), o = s;
      a().setInt32(e + 4 * 1, o, !0), a().setInt32(e + 4 * 0, c, !0);
    }, n.wbg.__wbg_getShaderParameter_cedb1ec0d8052eff = function(e, t, r) {
      return e.getShaderParameter(t, r >>> 0);
    }, n.wbg.__wbg_getUniformLocation_9cd213015cf8f29f = function(e, t, r, _) {
      const c = e.getUniformLocation(t, i(r, _));
      return g(c) ? 0 : d(c);
    }, n.wbg.__wbg_linkProgram_1f18bca817bb6edb = function(e, t) {
      e.linkProgram(t);
    }, n.wbg.__wbg_pixelStorei_2498331e094ff305 = function(e, t, r) {
      e.pixelStorei(t >>> 0, r);
    }, n.wbg.__wbg_polygonOffset_6d8d69a8d60e5b82 = function(e, t, r) {
      e.polygonOffset(t, r);
    }, n.wbg.__wbg_renderbufferStorage_8c3882aa73deada9 = function(e, t, r, _, c) {
      e.renderbufferStorage(t >>> 0, r >>> 0, _, c);
    }, n.wbg.__wbg_scissor_d06b14c4966727fa = function(e, t, r, _, c) {
      e.scissor(t, r, _, c);
    }, n.wbg.__wbg_shaderSource_d447b31057e4f64c = function(e, t, r, _) {
      e.shaderSource(t, i(r, _));
    }, n.wbg.__wbg_stencilFuncSeparate_55376d035e74caf1 = function(e, t, r, _, c) {
      e.stencilFuncSeparate(t >>> 0, r >>> 0, _, c >>> 0);
    }, n.wbg.__wbg_stencilMask_f55f160fc49b981a = function(e, t) {
      e.stencilMask(t >>> 0);
    }, n.wbg.__wbg_stencilMaskSeparate_578fd1281f54081e = function(e, t, r) {
      e.stencilMaskSeparate(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_stencilOpSeparate_ea6f96abd32aae5b = function(e, t, r, _, c) {
      e.stencilOpSeparate(t >>> 0, r >>> 0, _ >>> 0, c >>> 0);
    }, n.wbg.__wbg_texParameteri_83ad7181b62f4997 = function(e, t, r, _) {
      e.texParameteri(t >>> 0, r >>> 0, _);
    }, n.wbg.__wbg_uniform1f_509b4ba100d75456 = function(e, t, r) {
      e.uniform1f(t, r);
    }, n.wbg.__wbg_uniform1i_7f6e60c975d21e0a = function(e, t, r) {
      e.uniform1i(t, r);
    }, n.wbg.__wbg_uniform4f_f9a7809965964840 = function(e, t, r, _, c, o) {
      e.uniform4f(t, r, _, c, o);
    }, n.wbg.__wbg_useProgram_d4616618ac6d0652 = function(e, t) {
      e.useProgram(t);
    }, n.wbg.__wbg_vertexAttribPointer_fcbfe42523d724ca = function(e, t, r, _, c, o, f) {
      e.vertexAttribPointer(t >>> 0, r, _ >>> 0, c !== 0, o, f);
    }, n.wbg.__wbg_viewport_efc09c09d4f3cc48 = function(e, t, r, _, c) {
      e.viewport(t, r, _, c);
    }, n.wbg.__wbg_getSupportedProfiles_13c2c2008a14070f = function(e) {
      const t = e.getSupportedProfiles();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_setbox_0d838a2d268b7fac = function(e, t) {
      e.box = ["border-box", "content-box", "device-pixel-content-box"][t];
    }, n.wbg.__wbg_instanceof_Blob_a959e04f44007d16 = function(e) {
      let t;
      try {
        t = e instanceof Blob;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_size_8bb43f42080caff8 = function(e) {
      return e.size;
    }, n.wbg.__wbg_type_942eb9d383a1178d = function(e, t) {
      const r = t.type, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_newwithu8arraysequenceandoptions_c8bc456a23f02fca = function() {
      return u(function(e, t) {
        return new Blob(e, t);
      }, arguments);
    }, n.wbg.__wbg_arrayBuffer_c421744ca0e5f0bb = function(e) {
      return e.arrayBuffer();
    }, n.wbg.__wbg_items_10520d7d65f12510 = function(e) {
      return e.items;
    }, n.wbg.__wbg_files_a4b6a9811697ac84 = function(e) {
      const t = e.files;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_getData_b768ea3ff59e2a13 = function() {
      return u(function(e, t, r, _) {
        const c = t.getData(i(r, _)), o = m(c, b.__wbindgen_malloc, b.__wbindgen_realloc), f = s;
        a().setInt32(e + 4 * 1, f, !0), a().setInt32(e + 4 * 0, o, !0);
      }, arguments);
    }, n.wbg.__wbg_message_fde1ade05259137c = function(e, t) {
      const r = t.message, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_error_f4a23af7ac524546 = function(e) {
      return e.error;
    }, n.wbg.__wbg_addEventListener_e167f012cbedfa4e = function() {
      return u(function(e, t, r, _) {
        e.addEventListener(i(t, r), _);
      }, arguments);
    }, n.wbg.__wbg_removeEventListener_b6cef5ad085bea8f = function() {
      return u(function(e, t, r, _) {
        e.removeEventListener(i(t, r), _);
      }, arguments);
    }, n.wbg.__wbg_state_b863826253700666 = function() {
      return u(function(e) {
        return e.state;
      }, arguments);
    }, n.wbg.__wbg_back_2b44401f98571e5e = function() {
      return u(function(e) {
        e.back();
      }, arguments);
    }, n.wbg.__wbg_forward_5d07c36d03f1d798 = function() {
      return u(function(e) {
        e.forward();
      }, arguments);
    }, n.wbg.__wbg_pushState_fc8b2d0c45854901 = function() {
      return u(function(e, t, r, _, c, o) {
        e.pushState(t, i(r, _), c === 0 ? void 0 : i(c, o));
      }, arguments);
    }, n.wbg.__wbg_new_42acb42ec2ace97c = function() {
      return u(function(e) {
        return new ResizeObserver(e);
      }, arguments);
    }, n.wbg.__wbg_disconnect_1dbf7e19d9590abd = function(e) {
      e.disconnect();
    }, n.wbg.__wbg_observe_60f3631b2f7c6d8b = function(e, t, r) {
      e.observe(t, r);
    }, n.wbg.__wbg_new_641501f88c20bbcd = function() {
      return u(function(e) {
        return new EncodedVideoChunk(e);
      }, arguments);
    }, n.wbg.__wbg_instanceof_HtmlInputElement_88bf515ab1d9511d = function(e) {
      let t;
      try {
        t = e instanceof HTMLInputElement;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_setaccept_ecbe2b14b78fc505 = function(e, t, r) {
      e.accept = i(t, r);
    }, n.wbg.__wbg_setautofocus_7aec271950af807b = function(e, t) {
      e.autofocus = t !== 0;
    }, n.wbg.__wbg_files_b94d8f21e2b53924 = function(e) {
      const t = e.files;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_setmultiple_d67da734cbada979 = function(e, t) {
      e.multiple = t !== 0;
    }, n.wbg.__wbg_settype_c348825948b36c71 = function(e, t, r) {
      e.type = i(t, r);
    }, n.wbg.__wbg_value_d4a95e7a0d390578 = function(e, t) {
      const r = t.value, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_setvalue_688819688274bec0 = function(e, t, r) {
      e.value = i(t, r);
    }, n.wbg.__wbg_instanceof_ResizeObserverEntry_2c660d999b961603 = function(e) {
      let t;
      try {
        t = e instanceof ResizeObserverEntry;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_contentRect_c1a9045c459744d9 = function(e) {
      return e.contentRect;
    }, n.wbg.__wbg_contentBoxSize_a2d93ded171ea1de = function(e) {
      return e.contentBoxSize;
    }, n.wbg.__wbg_devicePixelContentBoxSize_8d531ca6a4331b28 = function(e) {
      return e.devicePixelContentBoxSize;
    }, n.wbg.__wbg_getItem_cab39762abab3e70 = function() {
      return u(function(e, t, r, _) {
        const c = t.getItem(i(r, _));
        var o = g(c) ? 0 : m(c, b.__wbindgen_malloc, b.__wbindgen_realloc), f = s;
        a().setInt32(e + 4 * 1, f, !0), a().setInt32(e + 4 * 0, o, !0);
      }, arguments);
    }, n.wbg.__wbg_setItem_9482185c870abba6 = function() {
      return u(function(e, t, r, _, c) {
        e.setItem(i(t, r), i(_, c));
      }, arguments);
    }, n.wbg.__wbg_delete_0441826dbfb45509 = function() {
      return u(function(e, t, r) {
        delete e[i(t, r)];
      }, arguments);
    }, n.wbg.__wbg_touches_91ecfe75e4e0bff0 = function(e) {
      return e.touches;
    }, n.wbg.__wbg_changedTouches_8a2627b3dec12eed = function(e) {
      return e.changedTouches;
    }, n.wbg.__wbg_setbody_734cb3d7ee8e6e96 = function(e, t) {
      e.body = t;
    }, n.wbg.__wbg_setmethod_dc68a742c2db5c6a = function(e, t, r) {
      e.method = i(t, r);
    }, n.wbg.__wbg_setmode_a781aae2bd3df202 = function(e, t) {
      e.mode = ["same-origin", "no-cors", "cors", "navigate"][t];
    }, n.wbg.__wbg_drawArraysInstancedANGLE_7c668fc363789760 = function(e, t, r, _, c) {
      e.drawArraysInstancedANGLE(t >>> 0, r, _, c);
    }, n.wbg.__wbg_drawElementsInstancedANGLE_7d0baa058556f76c = function(e, t, r, _, c, o) {
      e.drawElementsInstancedANGLE(t >>> 0, r, _ >>> 0, c, o);
    }, n.wbg.__wbg_vertexAttribDivisorANGLE_ff0ade84fc10084b = function(e, t, r) {
      e.vertexAttribDivisorANGLE(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_data_ee8c1a738c70cbe1 = function(e, t) {
      const r = t.data;
      var _ = g(r) ? 0 : m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_length_dbcf0a2509bc8271 = function(e) {
      return e.length;
    }, n.wbg.__wbg_get_39fc1e9743f29cdd = function(e, t) {
      const r = e[t >>> 0];
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_preventDefault_c55d86c27b2dfa6e = function(e) {
      e.preventDefault();
    }, n.wbg.__wbg_stopPropagation_dd0d50059627b362 = function(e) {
      e.stopPropagation();
    }, n.wbg.__wbg_set_b3c7c6d2e5e783d6 = function() {
      return u(function(e, t, r, _, c) {
        e.set(i(t, r), i(_, c));
      }, arguments);
    }, n.wbg.__wbg_clientX_3967ecd5e962e1b2 = function(e) {
      return e.clientX;
    }, n.wbg.__wbg_clientY_37d418b8d9c0bb52 = function(e) {
      return e.clientY;
    }, n.wbg.__wbg_ctrlKey_957c6c31b62b4550 = function(e) {
      return e.ctrlKey;
    }, n.wbg.__wbg_shiftKey_8c0f9a5ca3ff8f93 = function(e) {
      return e.shiftKey;
    }, n.wbg.__wbg_altKey_d3fbce7596aac8cf = function(e) {
      return e.altKey;
    }, n.wbg.__wbg_metaKey_be0158b14b1cef4a = function(e) {
      return e.metaKey;
    }, n.wbg.__wbg_button_460cdec9f2512a91 = function(e) {
      return e.button;
    }, n.wbg.__wbg_instanceof_ResizeObserverSize_200bcfcb71907f3f = function(e) {
      let t;
      try {
        t = e instanceof ResizeObserverSize;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_inlineSize_322ab111c2b5c9e3 = function(e) {
      return e.inlineSize;
    }, n.wbg.__wbg_blockSize_981c4dfa6e1263a8 = function(e) {
      return e.blockSize;
    }, n.wbg.__wbg_identifier_e39f89e9c0a1a3fc = function(e) {
      return e.identifier;
    }, n.wbg.__wbg_clientX_6ea27dc5cef626dd = function(e) {
      return e.clientX;
    }, n.wbg.__wbg_clientY_78f18a39f2f06125 = function(e) {
      return e.clientY;
    }, n.wbg.__wbg_force_f43e873103b4f9c8 = function(e) {
      return e.force;
    }, n.wbg.__wbg_setdata_15d5fc7ac2d677ba = function(e, t) {
      e.data = t;
    }, n.wbg.__wbg_settimestamp_d47750cc8a1c3d3a = function(e, t) {
      e.timestamp = t;
    }, n.wbg.__wbg_settype_b2524af382b4b097 = function(e, t) {
      e.type = ["key", "delta"][t];
    }, n.wbg.__wbg_setduration_611fb9e156dff581 = function(e, t) {
      e.duration = t;
    }, n.wbg.__wbg_writeText_20fb3f7393d34052 = function(e, t, r) {
      return e.writeText(i(t, r));
    }, n.wbg.__wbg_type_2716f55e3b73bcf3 = function(e, t) {
      const r = t.type, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_length_f2469772b8ec9ea3 = function(e) {
      return e.length;
    }, n.wbg.__wbg_get_6d8ff52d2078d871 = function(e, t) {
      const r = e[t >>> 0];
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_matches_42eb40a28a316d0e = function(e) {
      return e.matches;
    }, n.wbg.__wbg_matches_95beaf2233aaf53d = function(e) {
      return e.matches;
    }, n.wbg.__wbg_clipboard_0d7b5c390c14b0e6 = function(e) {
      return e.clipboard;
    }, n.wbg.__wbg_userAgent_58dedff4303aeb66 = function() {
      return u(function(e, t) {
        const r = t.userAgent, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_now_a69647afb1f66247 = function(e) {
      return e.now();
    }, n.wbg.__wbg_name_ed3cda975cce080d = function(e, t) {
      const r = t.name, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_lastModified_74d26354812e6299 = function(e) {
      return e.lastModified;
    }, n.wbg.__wbg_instanceof_HtmlAnchorElement_7a88f0b97085fa30 = function(e) {
      let t;
      try {
        t = e instanceof HTMLAnchorElement;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_setdownload_c4a56cf2790f498a = function(e, t, r) {
      e.download = i(t, r);
    }, n.wbg.__wbg_sethref_e76addd808540f69 = function(e, t, r) {
      e.href = i(t, r);
    }, n.wbg.__wbg_videoWidth_5f4190ae93af0dd6 = function(e) {
      return e.videoWidth;
    }, n.wbg.__wbg_videoHeight_4fb4bdd27e02263a = function(e) {
      return e.videoHeight;
    }, n.wbg.__wbg_href_9c2fe204628af7a3 = function() {
      return u(function(e, t) {
        const r = t.href, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_origin_648082c4831a5be8 = function() {
      return u(function(e, t) {
        const r = t.origin, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_protocol_787951293a197961 = function() {
      return u(function(e, t) {
        const r = t.protocol, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_host_a46347409a9511bd = function() {
      return u(function(e, t) {
        const r = t.host, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_hostname_d7ff17205929a46d = function() {
      return u(function(e, t) {
        const r = t.hostname, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_port_aeb48b36b706a841 = function() {
      return u(function(e, t) {
        const r = t.port, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_pathname_6e6871539b48a0e5 = function() {
      return u(function(e, t) {
        const r = t.pathname, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_search_20c15d493b8602c5 = function() {
      return u(function(e, t) {
        const r = t.search, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_hash_313d7fdf42f6e7d3 = function() {
      return u(function(e, t) {
        const r = t.hash, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_assign_01c9de4343368001 = function() {
      return u(function(e, t, r) {
        e.assign(i(t, r));
      }, arguments);
    }, n.wbg.__wbg_byobRequest_b32c77640da946ac = function(e) {
      const t = e.byobRequest;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_close_aca7442e6619206b = function() {
      return u(function(e) {
        e.close();
      }, arguments);
    }, n.wbg.__wbg_length_a547e4226b069330 = function(e) {
      return e.length;
    }, n.wbg.__wbg_item_4a685286202e2739 = function(e, t) {
      const r = e.item(t >>> 0);
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_get_6bee5bc8192fd59e = function(e, t) {
      const r = e[t >>> 0];
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_new_ac9dbf743c2383ee = function() {
      return u(function() {
        return new URLSearchParams();
      }, arguments);
    }, n.wbg.__wbg_append_67f0e14e943b043f = function(e, t, r, _, c) {
      e.append(i(t, r), i(_, c));
    }, n.wbg.__wbg_set_7341de5a79099de7 = function(e, t, r, _, c) {
      e.set(i(t, r), i(_, c));
    }, n.wbg.__wbg_setcodec_37318daa485f1029 = function(e, t, r) {
      e.codec = i(t, r);
    }, n.wbg.__wbg_setcodedheight_37fdde863d4fed9d = function(e, t) {
      e.codedHeight = t >>> 0;
    }, n.wbg.__wbg_setcodedwidth_f14b86753e987841 = function(e, t) {
      e.codedWidth = t >>> 0;
    }, n.wbg.__wbg_setdescription_d536e2495a7cb4de = function(e, t) {
      e.description = t;
    }, n.wbg.__wbg_sethardwareacceleration_86551d0c91d501a1 = function(e, t) {
      e.hardwareAcceleration = ["no-preference", "prefer-hardware", "prefer-software"][t];
    }, n.wbg.__wbg_setoptimizeforlatency_8748c0101417bfb0 = function(e, t) {
      e.optimizeForLatency = t !== 0;
    }, n.wbg.__wbg_seterror_374f6871e211a404 = function(e, t) {
      e.error = t;
    }, n.wbg.__wbg_setoutput_2b1793bf3fab4a0f = function(e, t) {
      e.output = t;
    }, n.wbg.__wbg_instanceof_DomException_1bbe86882eadb549 = function(e) {
      let t;
      try {
        t = e instanceof DOMException;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_code_4a4b2516783729c7 = function(e) {
      return e.code;
    }, n.wbg.__wbg_instanceof_HtmlCanvasElement_1a96a01603ec2d8b = function(e) {
      let t;
      try {
        t = e instanceof HTMLCanvasElement;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_width_53a5bd0268e99485 = function(e) {
      return e.width;
    }, n.wbg.__wbg_setwidth_e371a8d6b16ebe84 = function(e, t) {
      e.width = t >>> 0;
    }, n.wbg.__wbg_height_6fb32e51e54037ae = function(e) {
      return e.height;
    }, n.wbg.__wbg_setheight_ba99ad2df4295e89 = function(e, t) {
      e.height = t >>> 0;
    }, n.wbg.__wbg_getContext_69ec873410cbba3c = function() {
      return u(function(e, t, r) {
        const _ = e.getContext(i(t, r));
        return g(_) ? 0 : d(_);
      }, arguments);
    }, n.wbg.__wbg_getContext_70d493702d2b8f3e = function() {
      return u(function(e, t, r, _) {
        const c = e.getContext(i(t, r), _);
        return g(c) ? 0 : d(c);
      }, arguments);
    }, n.wbg.__wbg_keyCode_b06f25cc98035ed1 = function(e) {
      return e.keyCode;
    }, n.wbg.__wbg_altKey_5a6eb49ec8194792 = function(e) {
      return e.altKey;
    }, n.wbg.__wbg_ctrlKey_319ff2374dc7f372 = function(e) {
      return e.ctrlKey;
    }, n.wbg.__wbg_shiftKey_f38dee34420e0d62 = function(e) {
      return e.shiftKey;
    }, n.wbg.__wbg_metaKey_00fdcfadf1968d45 = function(e) {
      return e.metaKey;
    }, n.wbg.__wbg_isComposing_1c9533ed199eaf7b = function(e) {
      return e.isComposing;
    }, n.wbg.__wbg_key_a626396efbca2b95 = function(e, t) {
      const r = t.key, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_instanceof_MessageEvent_9951ccea5e1f35a2 = function(e) {
      let t;
      try {
        t = e instanceof MessageEvent;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_data_5c47a6985fefc490 = function(e) {
      return e.data;
    }, n.wbg.__wbg_width_a7c8cb533b26f0bf = function(e) {
      return e.width;
    }, n.wbg.__wbg_setwidth_c20f1f8fcd5d93b4 = function(e, t) {
      e.width = t >>> 0;
    }, n.wbg.__wbg_height_affa017f56a8fb96 = function(e) {
      return e.height;
    }, n.wbg.__wbg_setheight_a5e39c9d97429299 = function(e, t) {
      e.height = t >>> 0;
    }, n.wbg.__wbg_getContext_bd2ece8a59fd4732 = function() {
      return u(function(e, t, r) {
        const _ = e.getContext(i(t, r));
        return g(_) ? 0 : d(_);
      }, arguments);
    }, n.wbg.__wbg_getContext_76f1b45238db4411 = function() {
      return u(function(e, t, r, _) {
        const c = e.getContext(i(t, r), _);
        return g(c) ? 0 : d(c);
      }, arguments);
    }, n.wbg.__wbg_instanceof_ReadableStream_7b49703629f1df3c = function(e) {
      let t;
      try {
        t = e instanceof ReadableStream;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_view_2a901bda0727aeb3 = function(e) {
      const t = e.view;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_respond_a799bab31a44f2d7 = function() {
      return u(function(e, t) {
        e.respond(t >>> 0);
      }, arguments);
    }, n.wbg.__wbg_drawBuffersWEBGL_ff53a7c3360f5716 = function(e, t) {
      e.drawBuffersWEBGL(t);
    }, n.wbg.__wbg_deltaX_7f4a9de8338c7ca6 = function(e) {
      return e.deltaX;
    }, n.wbg.__wbg_deltaY_606f12aa66daba69 = function(e) {
      return e.deltaY;
    }, n.wbg.__wbg_deltaMode_d6b849e45efd0f5e = function(e) {
      return e.deltaMode;
    }, n.wbg.__wbg_navigator_db73b5b11a0c5c93 = function(e) {
      return e.navigator;
    }, n.wbg.__wbg_clipboardData_93c130a72996456a = function(e) {
      const t = e.clipboardData;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_width_e7964a50b174d035 = function(e) {
      return e.width;
    }, n.wbg.__wbg_height_cd5c897b4d3fabe3 = function(e) {
      return e.height;
    }, n.wbg.__wbg_top_322638693276a225 = function(e) {
      return e.top;
    }, n.wbg.__wbg_right_8b5d6a4fd660b15f = function(e) {
      return e.right;
    }, n.wbg.__wbg_bottom_9c5a8538fdbb5e16 = function(e) {
      return e.bottom;
    }, n.wbg.__wbg_left_ec3af38bed003a86 = function(e) {
      return e.left;
    }, n.wbg.__wbg_dataTransfer_2fb708051ee2c64c = function(e) {
      const t = e.dataTransfer;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_bindVertexArrayOES_37868a5a4265ea0a = function(e, t) {
      e.bindVertexArrayOES(t);
    }, n.wbg.__wbg_createVertexArrayOES_84334a02da216381 = function(e) {
      const t = e.createVertexArrayOES();
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_deleteVertexArrayOES_e22f7a6baedc5300 = function(e, t) {
      e.deleteVertexArrayOES(t);
    }, n.wbg.__wbg_new_c6a9ff2b3f853101 = function() {
      return u(function(e) {
        return new VideoDecoder(e);
      }, arguments);
    }, n.wbg.__wbg_close_604d9311162d0976 = function() {
      return u(function(e) {
        e.close();
      }, arguments);
    }, n.wbg.__wbg_configure_ea3bd7b470b5f985 = function() {
      return u(function(e, t) {
        e.configure(t);
      }, arguments);
    }, n.wbg.__wbg_decode_322aa8c3136679d0 = function() {
      return u(function(e, t) {
        e.decode(t);
      }, arguments);
    }, n.wbg.__wbg_reset_946aa2e6c9cecbe2 = function() {
      return u(function(e) {
        e.reset();
      }, arguments);
    }, n.wbg.__wbg_error_09480e4aadca50ad = typeof console.error == "function" ? console.error : q("console.error"), n.wbg.__wbg_settype_b6ab7b74bd1908a1 = function(e, t, r) {
      e.type = i(t, r);
    }, n.wbg.__wbg_result_3869032b57f861ac = function() {
      return u(function(e) {
        return e.result;
      }, arguments);
    }, n.wbg.__wbg_setonload_71d51f79887a9257 = function(e, t) {
      e.onload = t;
    }, n.wbg.__wbg_setonloadend_0c9330e0569633c0 = function(e, t) {
      e.onloadend = t;
    }, n.wbg.__wbg_new_8515b7401632bd44 = function() {
      return u(function() {
        return new FileReader();
      }, arguments);
    }, n.wbg.__wbg_readAsArrayBuffer_6475a86a924a8856 = function() {
      return u(function(e, t) {
        e.readAsArrayBuffer(t);
      }, arguments);
    }, n.wbg.__wbg_width_151910f38d746773 = function(e) {
      return e.width;
    }, n.wbg.__wbg_height_c1b4ecc1cfed30aa = function(e) {
      return e.height;
    }, n.wbg.__wbg_state_fe5d8462e453ff63 = function(e) {
      return e.state;
    }, n.wbg.__wbg_read_e48a676fb81ea800 = function(e) {
      return e.read();
    }, n.wbg.__wbg_releaseLock_1d2d93e9dc8d76e2 = function(e) {
      e.releaseLock();
    }, n.wbg.__wbg_cancel_97a2795574a4f522 = function(e) {
      return e.cancel();
    }, n.wbg.__wbg_headers_7d46f181de2aa1dd = function(e) {
      return e.headers;
    }, n.wbg.__wbg_newwithstrandinit_a31c69e4cc337183 = function() {
      return u(function(e, t, r) {
        return new Request(i(e, t), r);
      }, arguments);
    }, n.wbg.__wbg_instanceof_Response_e91b7eb7c611a9ae = function(e) {
      let t;
      try {
        t = e instanceof Response;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_url_1bf85c8abeb8c92d = function(e, t) {
      const r = t.url, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_status_ae8de515694c5c7c = function(e) {
      return e.status;
    }, n.wbg.__wbg_ok_227b0624f5926a87 = function(e) {
      return e.ok;
    }, n.wbg.__wbg_statusText_2c9a12f90531c8ed = function(e, t) {
      const r = t.statusText, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_headers_5e283e8345689121 = function(e) {
      return e.headers;
    }, n.wbg.__wbg_body_40b0ed27714d00ce = function(e) {
      const t = e.body;
      return g(t) ? 0 : d(t);
    }, n.wbg.__wbg_arrayBuffer_a5fbad63cc7e663b = function() {
      return u(function(e) {
        return e.arrayBuffer();
      }, arguments);
    }, n.wbg.__wbg_setonopen_7e770c87269cae90 = function(e, t) {
      e.onopen = t;
    }, n.wbg.__wbg_setonerror_5ec4625df3060159 = function(e, t) {
      e.onerror = t;
    }, n.wbg.__wbg_setonclose_40f935717ad6ffcd = function(e, t) {
      e.onclose = t;
    }, n.wbg.__wbg_setonmessage_b670c12ea34acd8b = function(e, t) {
      e.onmessage = t;
    }, n.wbg.__wbg_setbinaryType_d164a0be4c212c9c = function(e, t) {
      e.binaryType = ["blob", "arraybuffer"][t];
    }, n.wbg.__wbg_new_0bf4a5b0632517ed = function() {
      return u(function(e, t) {
        return new WebSocket(i(e, t));
      }, arguments);
    }, n.wbg.__wbg_close_99bb12a22f16f79c = function() {
      return u(function(e) {
        e.close();
      }, arguments);
    }, n.wbg.__wbg_getPropertyValue_b0f0858c3b5f17dd = function() {
      return u(function(e, t, r, _) {
        const c = t.getPropertyValue(i(r, _)), o = m(c, b.__wbindgen_malloc, b.__wbindgen_realloc), f = s;
        a().setInt32(e + 4 * 1, f, !0), a().setInt32(e + 4 * 0, o, !0);
      }, arguments);
    }, n.wbg.__wbg_setProperty_ff389e5a7fb9910e = function() {
      return u(function(e, t, r, _, c) {
        e.setProperty(i(t, r), i(_, c));
      }, arguments);
    }, n.wbg.__wbg_instanceof_HtmlButtonElement_998267b26d794a1e = function(e) {
      let t;
      try {
        t = e instanceof HTMLButtonElement;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_isComposing_ca7496e67564f5b9 = function(e) {
      return e.isComposing;
    }, n.wbg.__wbg_appendChild_ac45d1abddf1b89b = function() {
      return u(function(e, t) {
        return e.appendChild(t);
      }, arguments);
    }, n.wbg.__wbg_get_fe289e3950b3978a = function(e, t) {
      const r = e[t >>> 0];
      return g(r) ? 0 : d(r);
    }, n.wbg.__wbg_close_cef2400b120c9c73 = function() {
      return u(function(e) {
        e.close();
      }, arguments);
    }, n.wbg.__wbg_enqueue_6f3d433b5e457aea = function() {
      return u(function(e, t) {
        e.enqueue(t);
      }, arguments);
    }, n.wbg.__wbg_href_f1d20018a97415a0 = function(e, t) {
      const r = t.href, _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbg_searchParams_8b40e0942f870b44 = function(e) {
      return e.searchParams;
    }, n.wbg.__wbg_new_33db4be5d9963ec1 = function() {
      return u(function(e, t) {
        return new URL(i(e, t));
      }, arguments);
    }, n.wbg.__wbg_createObjectURL_ca544150f40fb1bf = function() {
      return u(function(e, t) {
        const r = URL.createObjectURL(t), _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
        a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
      }, arguments);
    }, n.wbg.__wbg_displayWidth_d9aadf05c3b7f971 = function(e) {
      return e.displayWidth;
    }, n.wbg.__wbg_displayHeight_8f8335b85311e287 = function(e) {
      return e.displayHeight;
    }, n.wbg.__wbg_duration_af309291b596dd12 = function(e, t) {
      const r = t.duration;
      a().setFloat64(e + 8 * 1, g(r) ? 0 : r, !0), a().setInt32(e + 4 * 0, !g(r), !0);
    }, n.wbg.__wbg_timestamp_18f6858fe9b39044 = function(e, t) {
      const r = t.timestamp;
      a().setFloat64(e + 8 * 1, g(r) ? 0 : r, !0), a().setInt32(e + 4 * 0, !g(r), !0);
    }, n.wbg.__wbg_clone_a3397c70f7a8f1c5 = function() {
      return u(function(e) {
        return e.clone();
      }, arguments);
    }, n.wbg.__wbg_close_d40a9ae3f32e4879 = function(e) {
      e.close();
    }, n.wbg.__wbg_warn_456e247116388326 = function(e, t) {
      console.warn(i(e, t));
    }, n.wbg.__wbg_info_6f08d0ae71cce2c8 = function(e, t) {
      console.info(i(e, t));
    }, n.wbg.__wbg_debug_d5c129f717d49a7c = function(e, t) {
      console.debug(i(e, t));
    }, n.wbg.__wbg_trace_810ebc094b8171ef = function(e, t) {
      console.trace(i(e, t));
    }, n.wbg.__wbg_performance_a1b8bde2ee512264 = function(e) {
      return e.performance;
    }, n.wbg.__wbg_now_abd80e969af37148 = function(e) {
      return e.now();
    }, n.wbg.__wbg_crypto_70a96de3b6b73dac = function(e) {
      return e.crypto;
    }, n.wbg.__wbg_process_dd1577445152112e = function(e) {
      return e.process;
    }, n.wbg.__wbg_versions_58036bec3add9e6f = function(e) {
      return e.versions;
    }, n.wbg.__wbg_node_6a9d28205ed5b0d8 = function(e) {
      return e.node;
    }, n.wbg.__wbg_require_f05d779769764e82 = function() {
      return u(function() {
        return module.require;
      }, arguments);
    }, n.wbg.__wbg_msCrypto_adbc770ec9eca9c7 = function(e) {
      return e.msCrypto;
    }, n.wbg.__wbg_randomFillSync_e950366c42764a07 = function() {
      return u(function(e, t) {
        e.randomFillSync(t);
      }, arguments);
    }, n.wbg.__wbg_getRandomValues_3774744e221a22ad = function() {
      return u(function(e, t) {
        e.getRandomValues(t);
      }, arguments);
    }, n.wbg.__wbg_get_3baa728f9d58d3f6 = function(e, t) {
      return e[t >>> 0];
    }, n.wbg.__wbg_length_ae22078168b726f5 = function(e) {
      return e.length;
    }, n.wbg.__wbg_new_a220cf903aa02ca2 = function() {
      return new Array();
    }, n.wbg.__wbg_newnoargs_76313bd6ff35d0f2 = function(e, t) {
      return new Function(i(e, t));
    }, n.wbg.__wbg_next_de3e9db4440638b2 = function(e) {
      return e.next;
    }, n.wbg.__wbg_next_f9cb570345655b9a = function() {
      return u(function(e) {
        return e.next();
      }, arguments);
    }, n.wbg.__wbg_done_bfda7aa8f252b39f = function(e) {
      return e.done;
    }, n.wbg.__wbg_value_6d39332ab4788d86 = function(e) {
      return e.value;
    }, n.wbg.__wbg_iterator_888179a48810a9fe = function() {
      return Symbol.iterator;
    }, n.wbg.__wbg_get_224d16597dbbfd96 = function() {
      return u(function(e, t) {
        return Reflect.get(e, t);
      }, arguments);
    }, n.wbg.__wbg_call_1084a111329e68ce = function() {
      return u(function(e, t) {
        return e.call(t);
      }, arguments);
    }, n.wbg.__wbg_new_525245e2b9901204 = function() {
      return new Object();
    }, n.wbg.__wbg_self_3093d5d1f7bcb682 = function() {
      return u(function() {
        return self.self;
      }, arguments);
    }, n.wbg.__wbg_window_3bcfc4d31bc012f8 = function() {
      return u(function() {
        return window.window;
      }, arguments);
    }, n.wbg.__wbg_globalThis_86b222e13bdf32ed = function() {
      return u(function() {
        return globalThis.globalThis;
      }, arguments);
    }, n.wbg.__wbg_global_e5a3fe56f8be9485 = function() {
      return u(function() {
        return global.global;
      }, arguments);
    }, n.wbg.__wbg_at_5fa66069579ac579 = function(e, t) {
      return e.at(t);
    }, n.wbg.__wbg_set_673dda6c73d19609 = function(e, t, r) {
      e[t >>> 0] = r;
    }, n.wbg.__wbg_includes_7c12264f911567fe = function(e, t, r) {
      return e.includes(t, r);
    }, n.wbg.__wbg_isArray_8364a5371e9737d8 = function(e) {
      return Array.isArray(e);
    }, n.wbg.__wbg_of_4a1c869ef05b4b73 = function(e) {
      return Array.of(e);
    }, n.wbg.__wbg_push_37c89022f34c01ca = function(e, t) {
      return e.push(t);
    }, n.wbg.__wbg_instanceof_ArrayBuffer_61dfc3198373c902 = function(e) {
      let t;
      try {
        t = e instanceof ArrayBuffer;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_instanceof_Error_69bde193b0cc95e3 = function(e) {
      let t;
      try {
        t = e instanceof Error;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_new_796382978dfd4fb0 = function(e, t) {
      return new Error(i(e, t));
    }, n.wbg.__wbg_toString_9d18e102ca933e68 = function(e) {
      return e.toString();
    }, n.wbg.__wbg_call_89af060b4e1523f2 = function() {
      return u(function(e, t, r) {
        return e.call(t, r);
      }, arguments);
    }, n.wbg.__wbg_isSafeInteger_7f1ed56200d90674 = function(e) {
      return Number.isSafeInteger(e);
    }, n.wbg.__wbg_getTime_91058879093a1589 = function(e) {
      return e.getTime();
    }, n.wbg.__wbg_getTimezoneOffset_c9929a3cc94500fe = function(e) {
      return e.getTimezoneOffset();
    }, n.wbg.__wbg_new_7982fb43cfca37ae = function(e) {
      return new Date(e);
    }, n.wbg.__wbg_new0_65387337a95cf44d = function() {
      return /* @__PURE__ */ new Date();
    }, n.wbg.__wbg_now_b7a162010a9e75b4 = function() {
      return Date.now();
    }, n.wbg.__wbg_instanceof_Object_b80213ae6cc9aafb = function(e) {
      let t;
      try {
        t = e instanceof Object;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_entries_7a0e06255456ebcd = function(e) {
      return Object.entries(e);
    }, n.wbg.__wbg_is_009b1ef508712fda = function(e, t) {
      return Object.is(e, t);
    }, n.wbg.__wbg_toString_e17a6671146f47c1 = function(e) {
      return e.toString();
    }, n.wbg.__wbg_valueOf_d5ba0a54a2aa5615 = function(e) {
      return e.valueOf();
    }, n.wbg.__wbg_instanceof_TypeError_eeccd04a800fcce2 = function(e) {
      let t;
      try {
        t = e instanceof TypeError;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_new_0c0bc0380537cd80 = function(e, t) {
      return new TypeError(i(e, t));
    }, n.wbg.__wbg_new_b85e72ed1bfd57f9 = function(e, t) {
      try {
        var r = { a: e, b: t }, _ = (o, f) => {
          const w = r.a;
          r.a = 0;
          try {
            return be(w, r.b, o, f);
          } finally {
            r.a = w;
          }
        };
        return new Promise(_);
      } finally {
        r.a = r.b = 0;
      }
    }, n.wbg.__wbg_resolve_570458cb99d56a43 = function(e) {
      return Promise.resolve(e);
    }, n.wbg.__wbg_catch_a279b1da46d132d8 = function(e, t) {
      return e.catch(t);
    }, n.wbg.__wbg_then_95e6edc0f89b73b1 = function(e, t) {
      return e.then(t);
    }, n.wbg.__wbg_then_876bb3c633745cc6 = function(e, t, r) {
      return e.then(t, r);
    }, n.wbg.__wbg_buffer_b7b08af79b0b0974 = function(e) {
      return e.buffer;
    }, n.wbg.__wbg_newwithbyteoffsetandlength_634ada0fd17e2e96 = function(e, t, r) {
      return new Int8Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_newwithbyteoffsetandlength_b5293b0eedbac651 = function(e, t, r) {
      return new Int16Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_newwithbyteoffsetandlength_c89d62ca194b7f14 = function(e, t, r) {
      return new Int32Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_newwithbyteoffsetandlength_8a2cb9ca96b27ec9 = function(e, t, r) {
      return new Uint8Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_new_ea1883e1e5e86686 = function(e) {
      return new Uint8Array(e);
    }, n.wbg.__wbg_set_d1e79e2388520f18 = function(e, t, r) {
      e.set(t, r >>> 0);
    }, n.wbg.__wbg_length_8339fcf5d8ecd12e = function(e) {
      return e.length;
    }, n.wbg.__wbg_newwithbyteoffsetandlength_bd3d5191e8925067 = function(e, t, r) {
      return new Uint16Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_newwithbyteoffsetandlength_874df3e29cb555f9 = function(e, t, r) {
      return new Uint32Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_newwithbyteoffsetandlength_a69c63d7671a5dbf = function(e, t, r) {
      return new Float32Array(e, t >>> 0, r >>> 0);
    }, n.wbg.__wbg_instanceof_Uint8Array_247a91427532499e = function(e) {
      let t;
      try {
        t = e instanceof Uint8Array;
      } catch {
        t = !1;
      }
      return t;
    }, n.wbg.__wbg_newwithlength_ec548f448387c968 = function(e) {
      return new Uint8Array(e >>> 0);
    }, n.wbg.__wbg_buffer_0710d1b9dbe2eea6 = function(e) {
      return e.buffer;
    }, n.wbg.__wbg_subarray_7c2e3576afe181d1 = function(e, t, r) {
      return e.subarray(t >>> 0, r >>> 0);
    }, n.wbg.__wbg_byteLength_850664ef28f3e42f = function(e) {
      return e.byteLength;
    }, n.wbg.__wbg_byteOffset_ea14c35fa6de38cc = function(e) {
      return e.byteOffset;
    }, n.wbg.__wbg_set_eacc7d73fefaafdf = function() {
      return u(function(e, t, r) {
        return Reflect.set(e, t, r);
      }, arguments);
    }, n.wbg.__wbindgen_debug_string = function(e, t) {
      const r = L(t), _ = m(r, b.__wbindgen_malloc, b.__wbindgen_realloc), c = s;
      a().setInt32(e + 4 * 1, c, !0), a().setInt32(e + 4 * 0, _, !0);
    }, n.wbg.__wbindgen_throw = function(e, t) {
      throw new Error(i(e, t));
    }, n.wbg.__wbindgen_memory = function() {
      return b.memory;
    }, n.wbg.__wbindgen_closure_wrapper1304 = function(e, t, r) {
      return x(e, t, 90, N);
    }, n.wbg.__wbindgen_closure_wrapper1306 = function(e, t, r) {
      return x(e, t, 90, X);
    }, n.wbg.__wbindgen_closure_wrapper13003 = function(e, t, r) {
      return x(e, t, 5018, Y);
    }, n.wbg.__wbindgen_closure_wrapper13005 = function(e, t, r) {
      return x(e, t, 5018, z);
    }, n.wbg.__wbindgen_closure_wrapper13007 = function(e, t, r) {
      return x(e, t, 5018, z);
    }, n.wbg.__wbindgen_closure_wrapper17140 = function(e, t, r) {
      return x(e, t, 6494, $);
    }, n.wbg.__wbindgen_closure_wrapper17763 = function(e, t, r) {
      return x(e, t, 6761, Z);
    }, n.wbg.__wbindgen_closure_wrapper19712 = function(e, t, r) {
      return U(e, t, 7327, V);
    }, n.wbg.__wbindgen_closure_wrapper19714 = function(e, t, r) {
      return U(e, t, 7327, V);
    }, n.wbg.__wbindgen_closure_wrapper21948 = function(e, t, r) {
      return x(e, t, 8348, G);
    }, n.wbg.__wbindgen_closure_wrapper21950 = function(e, t, r) {
      return x(e, t, 8348, G);
    }, n.wbg.__wbindgen_closure_wrapper29873 = function(e, t, r) {
      return x(e, t, 11725, C);
    }, n.wbg.__wbindgen_closure_wrapper29875 = function(e, t, r) {
      return x(e, t, 11725, C);
    }, n.wbg.__wbindgen_closure_wrapper29877 = function(e, t, r) {
      return x(e, t, 11725, C);
    }, n.wbg.__wbindgen_closure_wrapper29879 = function(e, t, r) {
      return x(e, t, 11725, C);
    }, n.wbg.__wbindgen_closure_wrapper36596 = function(e, t, r) {
      return x(e, t, 14607, J);
    }, n.wbg.__wbindgen_closure_wrapper36839 = function(e, t, r) {
      return x(e, t, 14680, ee);
    }, n.wbg.__wbindgen_closure_wrapper36908 = function(e, t, r) {
      return x(e, t, 14714, te);
    }, n.wbg.__wbindgen_init_externref_table = function() {
      const e = b.__wbindgen_export_2, t = e.grow(4);
      e.set(0, void 0), e.set(t + 0, void 0), e.set(t + 1, null), e.set(t + 2, !0), e.set(t + 3, !1);
    }, n;
  }
  function K(n, e) {
    return b = n.exports, O.__wbindgen_wasm_module = e, I = null, k = null, F = null, D = null, P = null, b.__wbindgen_start(), b;
  }
  function de(n) {
    if (b !== void 0) return b;
    typeof n < "u" && Object.getPrototypeOf(n) === Object.prototype ? { module: n } = n : console.warn("using deprecated parameters for `initSync()`; pass a single object instead");
    const e = H();
    n instanceof WebAssembly.Module || (n = new WebAssembly.Module(n));
    const t = new WebAssembly.Instance(n, e);
    return K(t, n);
  }
  async function O(n) {
    if (b !== void 0) return b;
    typeof n < "u" && Object.getPrototypeOf(n) === Object.prototype ? { module_or_path: n } = n : console.warn("using deprecated parameters for the initialization function; pass a single object instead");
    const e = H();
    (typeof n == "string" || typeof Request == "function" && n instanceof Request || typeof URL == "function" && n instanceof URL) && (n = fetch(n));
    const { instance: t, module: r } = await se(await n, e);
    return K(t, r);
  }
  function le() {
    O.__wbindgen_wasm_module = null, b = null, cachedFloat32Memory0 = null, cachedFloat64Memory0 = null, cachedInt32Memory0 = null, cachedUint32Memory0 = null, cachedUint8Memory0 = null;
  }
  return Object.assign(O, { initSync: de, deinit: le }, A);
}
export {
  me as default
};
