var pop = {
  isIOS:
    (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) ||
    ("MacIntel" === navigator.platform && navigator.maxTouchPoints > 1),
  isChrome: /chrome/i.test(navigator.userAgent),
  isFF: /firefox/i.test(navigator.userAgent),
  addEvent: function (t, e, n) {
    return null != t.addEventListener
      ? t.addEventListener(e, n, !1)
      : null != t.attachEvent
      ? t.attachEvent("on" + e, n)
      : (t[e] = n);
  },
  removeEvent: function (t, e, n) {
    return null != t.removeEventListener
      ? t.removeEventListener(e, n)
      : null != t.detachEvent
      ? t.detachEvent("on" + e, n)
      : (t[e] = null);
  },
  addPopupAnimationEndEvent: function (t, e) {
    var n = (function (t, e) {
      return function () {
        e(t);
      };
    })(t, e);
    this.addEvent(t, "animationend", n),
      this.addEvent(t, "oanimationend", n),
      this.addEvent(t, "webkitAnimationEnd", n),
      this.addEvent(t, "MSAnimationEnd", n),
      (t.fn = n);
  },
  removePopupAnimationEndEvent: function (t) {
    this.removeEvent(t, "animationend", t.fn),
      this.removeEvent(t, "oanimationend", t.fn),
      this.removeEvent(t, "webkitAnimationEnd", t.fn),
      this.removeEvent(t, "MSAnimationEnd", t.fn),
      (t.fn = null);
  },
  prop: function (t, e, n) {
    var i = void 0;
    "Transform" === e &&
      (i = t.getAttribute("data-popup-transform")) &&
      (n.length && (n += " "), (n += i));
    for (var o = "Webkit Moz O ms Khtml".split(" "), s = 0; s < o.length; s++)
      if (void 0 !== t.style[o[s] + e]) return void (t.style[o[s] + e] = n);
    void 0 === t.style[e.toLowerCase()] || (t.style[e.toLowerCase()] = n);
  },
  animationSupport: function () {
    if (null != this.animations) return this.animations;
    var t = document.createElement("div");
    if (void 0 !== t.style.animationName) return (this.animations = !0);
    for (var e = "Webkit Moz O ms Khtml".split(" "), n = 0; n < e.length; n++)
      if (void 0 !== t.style[e[n] + "AnimationName"])
        return (this.animations = !0);
    return (this.animations = !1);
  },
  popupFadeIn: function (t) {
    (t.style.opacity = 1),
      this.removeClass(t, "fadeIn"),
      t.offsetWidth,
      this.removePopupAnimationEndEvent(t);
  },
  popupFadeOut: function (t) {
    (t.style.visibility = "hidden"),
      this.prop(t, "Transform", "translate3d(-999999px,0,0)"),
      (t.style.opacity = 0),
      this.removeClass(t, "fadeOut"),
      t.offsetWidth,
      this.removePopupAnimationEndEvent(t);
  },
  closeGroup: function (t) {
    if (0 == t.hasAttribute("data-popup-group")) return !0;
    for (
      var e = t.getAttribute("data-popup-group"),
        n = document.getElementsByClassName("popup"),
        i = n.length - 1;
      i >= 0;
      i--
    )
      for (var o = n[i]; o != t && o != document; ) {
        if (o.getAttribute("data-popup-group") === e) {
          if (!1 !== this.isOpen(o)) this.closePopup(o.id);
          else if (o.hasAttribute("data-popup-open")) return !1;
          break;
        }
        o = o.parentNode;
      }
    return !0;
  },
  show: function (t) {
    var e = document.getElementById(t);
    this.prop(e, "Transform", "");
  },
  openPopup: function (t, e) {
    void 0 !== e && e.stopImmediatePropagation();
    var n = document.getElementById(t);
    if (null === n || !this.closeGroup(n)) return !1;
    var i = this.canOpen(n);
    if (!1 === i) return !1;
    if (null != i) wl.doAnimate(i);
    else {
      if (!this.hasClass(n, "animm")) {
        var o = n.querySelector(".animm");
        null != o && (o.style.visibility = "visible");
      }
      (n.style.visibility = "visible"), (n.style.opacity = 1);
    }
    var s = n.querySelector(".popup"),
      a = (null != s ? s : n).children[0];
    void 0 !== a &&
      "scroll" === window.getComputedStyle(a).getPropertyValue("overflow") &&
      ((a.style.overflow = "hidden"), a.offsetWidth, (a.style.overflow = "")),
      n.setAttribute("data-popup-open", !0);
    var r = n.getAttribute("data-popup-type");
    if (r > 0) {
      if (null != i) {
        var u = n.getAttribute("data-anim");
        null !== u && u.length
          ? (u = u.split(";"))
          : ((u = [i.style.animationDuration, i.style.animationDelay]),
            n.setAttribute("data-anim", u.join(";"))),
          (n.style.animationDuration =
            n.style["-webkit-animation-duration"] =
            n.style["-moz-animation-duration"] =
              u[0]),
          (n.style.animationDelay =
            n.style["-webkit-animation-delay"] =
            n.style["-moz-animation-delay"] =
              u[1]),
          this.removeClass(n, "fadeOut"),
          this.addClass(n, "fadeIn"),
          (n.style.visibility = "visible"),
          this.addPopupAnimationEndEvent(n, this.popupFadeIn.bind(this));
      }
      if (1 == r) {
        var l = document.body,
          p = document.documentElement.clientWidth - window.innerWidth,
          d = window.getComputedStyle(l).getPropertyValue("min-width");
        "0px" !== d &&
          (d = parseInt(d) * this.z()) > document.documentElement.clientWidth &&
          (p += parseInt(d) - document.documentElement.clientWidth) > 0 &&
          (p = 0),
          l.style.setProperty("--sw", parseInt(p) + "px"),
          (n.escapePressed = (function (t) {
            return function (e) {
              var n;
              pop.isOpen(t) &&
                (n = t.getAttribute("onclick")) &&
                n.length > 0 &&
                27 == e.keyCode &&
                t.escapePressed &&
                (pop.closePopup(t.id),
                pop.removeEvent(document, "keyup", t.escapePressed),
                (t.escapePressed = void 0));
            };
          })(n)),
          this.addEvent(document, "keyup", n.escapePressed),
          this.updateAlign(),
          this.addClass(l, "modal"),
          n.addEventListener &&
            n.addEventListener(
              "touchstart",
              (this.preventscroll = (function (t) {
                return function (e) {
                  if (e.target == t) {
                    var n = t.getAttribute("onclick");
                    n && n.length > 0 && pop.closePopup(t.id);
                  }
                };
              })(n))
            );
      }
    }
    if (
      (this.prop(n, "Transform", ""), null != this.hook && null != this.hook[t])
    )
      for (var m = this.hook[t], h = m.length, c = 0; c < h; c++)
        null != m[c].open && m[c].open();
    var v = document.createEvent("Event");
    return v.initEvent("scroll", !0, !0), window.dispatchEvent(v), !1;
  },
  isOpen: function (t) {
    var e;
    return (
      !(
        !t.hasAttribute("data-popup-open") ||
        t.fn ||
        this.hasClass(t, "animated") ||
        (null != (e = t.querySelector(".animm")) &&
          this.hasClass(e, "animated"))
      ) && e
    );
  },
  canOpen: function (t) {
    var e = void 0;
    return (
      this.animationSupport() &&
        (e = this.hasClass(t, "animm") ? t : t.querySelector(".animm")),
      !(
        t.hasAttribute("data-popup-open") ||
        null != t.fn ||
        this.hasClass(t, "animated") ||
        (null != e && this.hasClass(e, "animated"))
      ) && e
    );
  },
  openClosePopup: function (t, e) {
    var n = document.getElementById(t);
    return (
      !1 === this.isOpen(n) ? this.openPopup(t, e) : this.closePopup(t, e), !1
    );
  },
  closePopup: function (t, e) {
    void 0 !== e && e.stopImmediatePropagation();
    var n = document.getElementById(t),
      i = this.isOpen(n);
    if (!1 === i) return !1;
    var o = n.getAttribute("data-popup-type");
    if (
      (n.removeAttribute("data-popup-open"),
      this.animationSupport() &&
        (i = this.hasClass(n, "animm") ? n : n.querySelector(".animm")),
      null != i && wl.doAnimate(i, 1),
      n != i)
    )
      if (null != i && 0 != o) {
        var s = n.getAttribute("data-anim").split(";");
        (n.style.animationDuration =
          n.style["-webkit-animation-duration"] =
          n.style["-moz-animation-duration"] =
            s[0]),
          (n.style.animationDelay =
            n.style["-webkit-animation-delay"] =
            n.style["-moz-animation-delay"] =
              s[1]),
          this.removeClass(n, "fadeIn"),
          this.addClass(n, "fadeOut"),
          this.addPopupAnimationEndEvent(n, this.popupFadeOut.bind(this));
      } else
        (n.style.visibility = "hidden"),
          this.prop(n, "Transform", "translate3d(-999999px,0,0)"),
          (n.style.opacity = 0);
    this.updateAlign(!0);
    var a = document.body;
    if (
      (this.removeClass(a, "modal"),
      a.style.setProperty("--sw", "0px"),
      n.removeEventListener &&
        n.removeEventListener("touchstart", this.preventScroll),
      null != this.hook && null != this.hook[t])
    )
      for (var r = this.hook[t], u = r.length, l = 0; l < u; l++)
        null != r[l].close && r[l].close();
    return !1;
  },
  overPopup: function (t, e) {
    var n = document.getElementById(e);
    !1 === this.isOpen(n)
      ? this.openPopup(e)
      : t.oo && (clearTimeout(t.oo), (t.oo = void 0));
  },
  overoutPopup: function (t, e) {
    var n = (function (t, e) {
      return function () {
        var i,
          o = null != e ? document.getElementById(e) : void 0;
        !t.oo ||
        (null != o &&
          !1 !== pop.isOpen(o) &&
          pop.isOver((i = o.querySelector(".popup")) ? i : o))
          ? (t.oo = setTimeout(n, t.oo ? 100 : 1))
          : ((t.oo = void 0),
            null != e &&
              (!1 !== pop.isOpen(o)
                ? pop.closePopup(e)
                : o.hasAttribute("data-popup-open") &&
                  (t.oo = setTimeout(n, 100))));
      };
    })(t, e);
    t.oo && (clearTimeout(t.oo), (t.oo = void 0)), n();
  },
  mouseMove: function (t) {
    (this.mouseX = t.clientX), (this.mouseY = t.clientY);
  },
  touchStart: function (t, e, n) {
    t.touches.length &&
      ((this.mouseX = t.touches[0].clientX),
      (this.mouseY = t.touches[0].clientY)),
      this.overPopup(e, n);
  },
  touchMove: function (t) {
    t.touches.length &&
      ((this.mouseX = t.touches[0].clientX),
      (this.mouseY = t.touches[0].clientY));
  },
  touchEnd: function (t, e, n) {
    t.touches.length &&
      ((this.mouseX = t.touches[0].clientX),
      (this.mouseY = t.touches[0].clientY));
  },
  isOver: function (t) {
    var e = t.getBoundingClientRect();
    if (!this.isFF) {
      var n = this.z();
      (e = {
        left: e.left * n,
        right: e.right * n,
        top: e.top * n,
        bottom: e.bottom * n,
      }),
        this.isChrome ||
          ((e.top += window.scrollY * (n - 1)),
          (e.bottom += window.scrollY * (n - 1)));
    }
    return (
      this.mouseX >= parseInt(e.left) &&
      this.mouseX <= parseInt(e.right) &&
      this.mouseY >= parseInt(e.top) &&
      this.mouseY <= parseInt(e.bottom)
    );
  },
  hasClass: function (t, e) {
    var n = t.classList;
    return null != n
      ? n.contains(e)
      : (" " + t.className + " ").indexOf(" " + e + " ") > -1;
  },
  addClass: function (t, e) {
    var n = t.classList;
    null != n ? n.add(e) : (t.className += " " + e);
  },
  removeClass: function (t, e) {
    if (null != (n = t.classList)) n.remove(e);
    else {
      var n,
        i = (n = t.className.split(" ")).indexOf(e);
      i >= 0 && (n.splice(i, 1), (t.className = n.join(" ")));
    }
  },
  addHook: function (t, e, n) {
    null == this.hook && (this.hook = {}),
      null == this.hook[t] && (this.hook[t] = []),
      this.hook[t].push({ open: e, close: n });
  },
  z: function () {
    var t = parseFloat(
      window.getComputedStyle(document.body).getPropertyValue("zoom")
    );
    return t || 1;
  },
  updateAlign: function (t) {
    if (this.isIOS) {
      var e = this.z(),
        n = document.body.style,
        i = n.cssText,
        o = i.indexOf("margin-top"),
        s = i.indexOf("position");
      if (o >= 0 && s >= 0 && (s = i.indexOf(";", s + 8)) >= 0) {
        var a = -parseInt(n.marginTop) * e;
        (i = i.substring(0, o) + i.substring(s + 1)),
          (n.cssText = i),
          window.scrollTo(0, a);
      }
      t ||
        ((i +=
          "margin-top:-" +
          (window.scrollY / e).toFixed(3) +
          "px;width:calc(100% - var(--sw));position:fixed;"),
        (n.cssText += i));
    }
  },
  init: function () {
    var t = function () {
      var t = pop.z(),
        e = (0.01 * window.innerHeight) / t;
      if (pop.vh !== e) {
        var n = document.body;
        (pop.vh = e),
          n.style.setProperty("--vh", e + "px"),
          pop.hasClass(n, "modal") && pop.updateAlign();
      }
    };
    if ("requestAnimationFrame" in window) {
      var e = function () {
        t(), requestAnimationFrame(e);
      };
      requestAnimationFrame(e);
    } else this.addEvent(window, "resize", t), t();
    this.addEvent(window, "mousemove", this.mouseMove.bind(this)),
      this.addEvent(window, "touchmove", this.touchMove.bind(this));
  },
};
pop.init();
