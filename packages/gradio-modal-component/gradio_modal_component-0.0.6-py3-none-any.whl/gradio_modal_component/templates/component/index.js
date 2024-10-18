const {
  SvelteComponent: de,
  assign: re,
  create_slot: ue,
  detach: me,
  element: be,
  get_all_dirty_from_scope: ge,
  get_slot_changes: he,
  get_spread_update: we,
  init: ke,
  insert: ye,
  safe_not_equal: ve,
  set_dynamic_element_data: V,
  set_style: v,
  toggle_class: L,
  transition_in: ee,
  transition_out: le,
  update_slot_base: ze
} = window.__gradio__svelte__internal;
function Se(t) {
  let e, l, n;
  const i = (
    /*#slots*/
    t[18].default
  ), a = ue(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1t38q2d"
    }
  ], c = {};
  for (let f = 0; f < o.length; f += 1)
    c = re(c, o[f]);
  return {
    c() {
      e = be(
        /*tag*/
        t[14]
      ), a && a.c(), V(
        /*tag*/
        t[14]
      )(e, c), L(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        t[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), v(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), v(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), v(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), v(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), v(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), v(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), v(e, "border-width", "var(--block-border-width)");
    },
    m(f, s) {
      ye(f, e, s), a && a.m(e, null), n = !0;
    },
    p(f, s) {
      a && a.p && (!n || s & /*$$scope*/
      131072) && ze(
        a,
        i,
        f,
        /*$$scope*/
        f[17],
        n ? he(
          i,
          /*$$scope*/
          f[17],
          s,
          null
        ) : ge(
          /*$$scope*/
          f[17]
        ),
        null
      ), V(
        /*tag*/
        f[14]
      )(e, c = we(o, [
        (!n || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!n || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!n || s & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-1t38q2d")) && { class: l }
      ])), L(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        f[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), s & /*height*/
      1 && v(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), s & /*width*/
      2 && v(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), s & /*variant*/
      16 && v(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), s & /*allow_overflow*/
      2048 && v(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && v(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), s & /*min_width*/
      8192 && v(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      n || (ee(a, f), n = !0);
    },
    o(f) {
      le(a, f), n = !1;
    },
    d(f) {
      f && me(e), a && a.d(f);
    }
  };
}
function Ce(t) {
  let e, l = (
    /*tag*/
    t[14] && Se(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(n, i) {
      l && l.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && l.p(n, i);
    },
    i(n) {
      e || (ee(l, n), e = !0);
    },
    o(n) {
      le(l, n), e = !1;
    },
    d(n) {
      l && l.d(n);
    }
  };
}
function je(t, e, l) {
  let { $$slots: n = {}, $$scope: i } = e, { height: a = void 0 } = e, { width: o = void 0 } = e, { elem_id: c = "" } = e, { elem_classes: f = [] } = e, { variant: s = "solid" } = e, { border_mode: r = "base" } = e, { padding: m = !0 } = e, { type: u = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: S = !1 } = e, { container: y = !0 } = e, { visible: j = !0 } = e, { allow_overflow: q = !0 } = e, { scale: b = null } = e, { min_width: g = 0 } = e, B = u === "fieldset" ? "fieldset" : "div";
  const I = (d) => {
    if (d !== void 0) {
      if (typeof d == "number")
        return d + "px";
      if (typeof d == "string")
        return d;
    }
  };
  return t.$$set = (d) => {
    "height" in d && l(0, a = d.height), "width" in d && l(1, o = d.width), "elem_id" in d && l(2, c = d.elem_id), "elem_classes" in d && l(3, f = d.elem_classes), "variant" in d && l(4, s = d.variant), "border_mode" in d && l(5, r = d.border_mode), "padding" in d && l(6, m = d.padding), "type" in d && l(16, u = d.type), "test_id" in d && l(7, w = d.test_id), "explicit_call" in d && l(8, S = d.explicit_call), "container" in d && l(9, y = d.container), "visible" in d && l(10, j = d.visible), "allow_overflow" in d && l(11, q = d.allow_overflow), "scale" in d && l(12, b = d.scale), "min_width" in d && l(13, g = d.min_width), "$$scope" in d && l(17, i = d.$$scope);
  }, [
    a,
    o,
    c,
    f,
    s,
    r,
    m,
    w,
    S,
    y,
    j,
    q,
    b,
    g,
    B,
    I,
    u,
    i,
    n
  ];
}
class qe extends de {
  constructor(e) {
    super(), ke(this, e, je, Ce, ve, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const Le = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], W = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Le.reduce(
  (t, { color: e, primary: l, secondary: n }) => ({
    ...t,
    [e]: {
      primary: W[e][l],
      secondary: W[e][n]
    }
  }),
  {}
);
const {
  SvelteComponent: Me,
  attr: D,
  create_slot: Ie,
  detach: Be,
  element: Ee,
  get_all_dirty_from_scope: Ne,
  get_slot_changes: He,
  init: Te,
  insert: Ye,
  null_to_empty: X,
  safe_not_equal: Ae,
  set_style: F,
  toggle_class: M,
  transition_in: De,
  transition_out: Fe,
  update_slot_base: Ge
} = window.__gradio__svelte__internal;
function Je(t) {
  let e, l, n = `calc(min(${/*min_width*/
  t[2]}px, 100%))`, i;
  const a = (
    /*#slots*/
    t[8].default
  ), o = Ie(
    a,
    t,
    /*$$scope*/
    t[7],
    null
  );
  return {
    c() {
      e = Ee("div"), o && o.c(), D(
        e,
        "id",
        /*elem_id*/
        t[3]
      ), D(e, "class", l = X(
        /*elem_classes*/
        t[4].join(" ")
      ) + " svelte-1m1obck"), M(
        e,
        "gap",
        /*gap*/
        t[1]
      ), M(
        e,
        "compact",
        /*variant*/
        t[6] === "compact"
      ), M(
        e,
        "panel",
        /*variant*/
        t[6] === "panel"
      ), M(e, "hide", !/*visible*/
      t[5]), F(
        e,
        "flex-grow",
        /*scale*/
        t[0]
      ), F(e, "min-width", n);
    },
    m(c, f) {
      Ye(c, e, f), o && o.m(e, null), i = !0;
    },
    p(c, [f]) {
      o && o.p && (!i || f & /*$$scope*/
      128) && Ge(
        o,
        a,
        c,
        /*$$scope*/
        c[7],
        i ? He(
          a,
          /*$$scope*/
          c[7],
          f,
          null
        ) : Ne(
          /*$$scope*/
          c[7]
        ),
        null
      ), (!i || f & /*elem_id*/
      8) && D(
        e,
        "id",
        /*elem_id*/
        c[3]
      ), (!i || f & /*elem_classes*/
      16 && l !== (l = X(
        /*elem_classes*/
        c[4].join(" ")
      ) + " svelte-1m1obck")) && D(e, "class", l), (!i || f & /*elem_classes, gap*/
      18) && M(
        e,
        "gap",
        /*gap*/
        c[1]
      ), (!i || f & /*elem_classes, variant*/
      80) && M(
        e,
        "compact",
        /*variant*/
        c[6] === "compact"
      ), (!i || f & /*elem_classes, variant*/
      80) && M(
        e,
        "panel",
        /*variant*/
        c[6] === "panel"
      ), (!i || f & /*elem_classes, visible*/
      48) && M(e, "hide", !/*visible*/
      c[5]), f & /*scale*/
      1 && F(
        e,
        "flex-grow",
        /*scale*/
        c[0]
      ), f & /*min_width*/
      4 && n !== (n = `calc(min(${/*min_width*/
      c[2]}px, 100%))`) && F(e, "min-width", n);
    },
    i(c) {
      i || (De(o, c), i = !0);
    },
    o(c) {
      Fe(o, c), i = !1;
    },
    d(c) {
      c && Be(e), o && o.d(c);
    }
  };
}
function Ke(t, e, l) {
  let { $$slots: n = {}, $$scope: i } = e, { scale: a = null } = e, { gap: o = !0 } = e, { min_width: c = 0 } = e, { elem_id: f = "" } = e, { elem_classes: s = [] } = e, { visible: r = !0 } = e, { variant: m = "default" } = e;
  return t.$$set = (u) => {
    "scale" in u && l(0, a = u.scale), "gap" in u && l(1, o = u.gap), "min_width" in u && l(2, c = u.min_width), "elem_id" in u && l(3, f = u.elem_id), "elem_classes" in u && l(4, s = u.elem_classes), "visible" in u && l(5, r = u.visible), "variant" in u && l(6, m = u.variant), "$$scope" in u && l(7, i = u.$$scope);
  }, [a, o, c, f, s, r, m, i, n];
}
let Oe = class extends Me {
  constructor(e) {
    super(), Te(this, e, Ke, Je, Ae, {
      scale: 0,
      gap: 1,
      min_width: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      variant: 6
    });
  }
};
const {
  SvelteComponent: Pe,
  append: k,
  attr: h,
  binding_callbacks: Z,
  create_component: te,
  create_slot: Qe,
  destroy_component: ne,
  detach: N,
  element: C,
  get_all_dirty_from_scope: Re,
  get_slot_changes: Ue,
  init: Ve,
  insert: H,
  listen: G,
  mount_component: fe,
  noop: We,
  run_all: Xe,
  safe_not_equal: Ze,
  set_data: K,
  set_style: z,
  space: E,
  text: O,
  toggle_class: p,
  transition_in: P,
  transition_out: Q,
  update_slot_base: pe
} = window.__gradio__svelte__internal;
function x(t) {
  let e, l, n;
  return {
    c() {
      e = C("div"), e.innerHTML = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9 1L1 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>', h(e, "class", "close svelte-30h6gz");
    },
    m(i, a) {
      H(i, e, a), l || (n = G(
        e,
        "click",
        /*close*/
        t[13]
      ), l = !0);
    },
    p: We,
    d(i) {
      i && N(e), l = !1, n();
    }
  };
}
function xe(t) {
  let e;
  const l = (
    /*#slots*/
    t[25].default
  ), n = Qe(
    l,
    t,
    /*$$scope*/
    t[29],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, a) {
      n && n.m(i, a), e = !0;
    },
    p(i, a) {
      n && n.p && (!e || a & /*$$scope*/
      536870912) && pe(
        n,
        l,
        i,
        /*$$scope*/
        i[29],
        e ? Ue(
          l,
          /*$$scope*/
          i[29],
          a,
          null
        ) : Re(
          /*$$scope*/
          i[29]
        ),
        null
      );
    },
    i(i) {
      e || (P(n, i), e = !0);
    },
    o(i) {
      Q(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function $e(t) {
  let e, l, n, i, a = (
    /*display_close_icon*/
    t[3] && x(t)
  );
  return n = new Oe({
    props: {
      elem_classes: ["centered-column"],
      $$slots: { default: [xe] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      a && a.c(), e = E(), l = C("div"), te(n.$$.fragment), h(l, "class", "modal-content svelte-30h6gz"), h(
        l,
        "style",
        /*contentStyle*/
        t[10]
      );
    },
    m(o, c) {
      a && a.m(o, c), H(o, e, c), H(o, l, c), fe(n, l, null), i = !0;
    },
    p(o, c) {
      /*display_close_icon*/
      o[3] ? a ? a.p(o, c) : (a = x(o), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null);
      const f = {};
      c & /*$$scope*/
      536870912 && (f.$$scope = { dirty: c, ctx: o }), n.$set(f), (!i || c & /*contentStyle*/
      1024) && h(
        l,
        "style",
        /*contentStyle*/
        o[10]
      );
    },
    i(o) {
      i || (P(n.$$.fragment, o), i = !0);
    },
    o(o) {
      Q(n.$$.fragment, o), i = !1;
    },
    d(o) {
      o && (N(e), N(l)), a && a.d(o), ne(n);
    }
  };
}
function $(t) {
  let e, l, n, i, a, o, c, f, s, r = (
    /*close_message_style*/
    t[6].confirm_text + ""
  ), m, u, w, S = (
    /*close_message_style*/
    t[6].cancel_text + ""
  ), y, j, q;
  return {
    c() {
      e = C("div"), l = C("div"), n = C("h3"), i = O(
        /*close_message*/
        t[5]
      ), a = E(), o = C("br"), c = E(), f = C("div"), s = C("button"), m = O(r), u = E(), w = C("button"), y = O(S), z(
        n,
        "color",
        /*close_message_style*/
        t[6].message_color
      ), h(n, "class", "svelte-30h6gz"), h(s, "class", "yes-button svelte-30h6gz"), z(
        s,
        "background-color",
        /*close_message_style*/
        t[6].confirm_bg_color
      ), z(
        s,
        "color",
        /*close_message_style*/
        t[6].confirm_text_color
      ), h(w, "class", "no-button svelte-30h6gz"), z(
        w,
        "background-color",
        /*close_message_style*/
        t[6].cancel_bg_color
      ), z(
        w,
        "color",
        /*close_message_style*/
        t[6].cancel_text_color
      ), h(f, "class", "confirmation-buttons svelte-30h6gz"), h(l, "class", "confirmation-content svelte-30h6gz"), z(
        l,
        "background-color",
        /*close_message_style*/
        t[6].modal_bg_color
      ), h(e, "class", "confirmation-modal svelte-30h6gz");
    },
    m(b, g) {
      H(b, e, g), k(e, l), k(l, n), k(n, i), k(l, a), k(l, o), k(l, c), k(l, f), k(f, s), k(s, m), k(f, u), k(f, w), k(w, y), j || (q = [
        G(
          s,
          "click",
          /*closeModal*/
          t[14]
        ),
        G(
          w,
          "click",
          /*cancelClose*/
          t[15]
        )
      ], j = !0);
    },
    p(b, g) {
      g & /*close_message*/
      32 && K(
        i,
        /*close_message*/
        b[5]
      ), g & /*close_message_style*/
      64 && z(
        n,
        "color",
        /*close_message_style*/
        b[6].message_color
      ), g & /*close_message_style*/
      64 && r !== (r = /*close_message_style*/
      b[6].confirm_text + "") && K(m, r), g & /*close_message_style*/
      64 && z(
        s,
        "background-color",
        /*close_message_style*/
        b[6].confirm_bg_color
      ), g & /*close_message_style*/
      64 && z(
        s,
        "color",
        /*close_message_style*/
        b[6].confirm_text_color
      ), g & /*close_message_style*/
      64 && S !== (S = /*close_message_style*/
      b[6].cancel_text + "") && K(y, S), g & /*close_message_style*/
      64 && z(
        w,
        "background-color",
        /*close_message_style*/
        b[6].cancel_bg_color
      ), g & /*close_message_style*/
      64 && z(
        w,
        "color",
        /*close_message_style*/
        b[6].cancel_text_color
      ), g & /*close_message_style*/
      64 && z(
        l,
        "background-color",
        /*close_message_style*/
        b[6].modal_bg_color
      );
    },
    d(b) {
      b && N(e), j = !1, Xe(q);
    }
  };
}
function e0(t) {
  let e, l, n, i, a, o, c, f;
  n = new qe({
    props: {
      allow_overflow: !1,
      elem_classes: ["modal-block"],
      $$slots: { default: [$e] },
      $$scope: { ctx: t }
    }
  });
  let s = (
    /*showConfirmation*/
    t[9] && $(t)
  );
  return {
    c() {
      e = C("div"), l = C("div"), te(n.$$.fragment), i = E(), s && s.c(), h(l, "class", "modal-container svelte-30h6gz"), h(
        l,
        "style",
        /*containerStyle*/
        t[11]
      ), h(e, "class", a = "modal " + /*elem_classes*/
      t[2].join(" ") + " svelte-30h6gz"), h(
        e,
        "id",
        /*elem_id*/
        t[1]
      ), h(
        e,
        "style",
        /*modalStyle*/
        t[12]
      ), p(e, "hide", !/*visible*/
      t[0]);
    },
    m(r, m) {
      H(r, e, m), k(e, l), fe(n, l, null), t[26](l), k(e, i), s && s.m(e, null), t[27](e), o = !0, c || (f = G(
        e,
        "click",
        /*click_handler*/
        t[28]
      ), c = !0);
    },
    p(r, [m]) {
      const u = {};
      m & /*$$scope, contentStyle, display_close_icon*/
      536871944 && (u.$$scope = { dirty: m, ctx: r }), n.$set(u), (!o || m & /*containerStyle*/
      2048) && h(
        l,
        "style",
        /*containerStyle*/
        r[11]
      ), /*showConfirmation*/
      r[9] ? s ? s.p(r, m) : (s = $(r), s.c(), s.m(e, null)) : s && (s.d(1), s = null), (!o || m & /*elem_classes*/
      4 && a !== (a = "modal " + /*elem_classes*/
      r[2].join(" ") + " svelte-30h6gz")) && h(e, "class", a), (!o || m & /*elem_id*/
      2) && h(
        e,
        "id",
        /*elem_id*/
        r[1]
      ), (!o || m & /*modalStyle*/
      4096) && h(
        e,
        "style",
        /*modalStyle*/
        r[12]
      ), (!o || m & /*elem_classes, visible*/
      5) && p(e, "hide", !/*visible*/
      r[0]);
    },
    i(r) {
      o || (P(n.$$.fragment, r), o = !0);
    },
    o(r) {
      Q(n.$$.fragment, r), o = !1;
    },
    d(r) {
      r && N(e), ne(n), t[26](null), s && s.d(), t[27](null), c = !1, f();
    }
  };
}
function l0(t, e, l) {
  let n, i, a, { $$slots: o = {}, $$scope: c } = e, { elem_id: f = "" } = e, { elem_classes: s = [] } = e, { visible: r = !1 } = e, { display_close_icon: m = !1 } = e, { close_on_esc: u } = e, { close_outer_click: w } = e, { close_message: S } = e, { bg_blur: y } = e, { width: j } = e, { height: q } = e, { content_width_percent: b } = e, { content_height_percent: g } = e, { content_padding: B } = e, { opacity_level: I } = e, { gradio: d } = e, { close_message_style: R = {
    message_color: "var(--body-text-color)",
    confirm_text: "Yes",
    cancel_text: "No",
    confirm_bg_color: "var(--primary-500)",
    cancel_bg_color: "var(--neutral-500)",
    confirm_text_color: "white",
    cancel_text_color: "white",
    modal_bg_color: "var(--background-fill-primary)"
  } } = e, T = null, Y = null, A = !1;
  const J = () => {
    S ? l(9, A = !0) : U();
  }, U = () => {
    l(0, r = !1), l(9, A = !1), d.dispatch("blur");
  }, ie = () => {
    l(9, A = !1);
  };
  document.addEventListener("keydown", (_) => {
    u && _.key === "Escape" && J();
  });
  function ae(_) {
    Z[_ ? "unshift" : "push"](() => {
      Y = _, l(8, Y);
    });
  }
  function oe(_) {
    Z[_ ? "unshift" : "push"](() => {
      T = _, l(7, T);
    });
  }
  const ce = (_) => {
    w && (_.target === T || _.target === Y) && J();
  };
  return t.$$set = (_) => {
    "elem_id" in _ && l(1, f = _.elem_id), "elem_classes" in _ && l(2, s = _.elem_classes), "visible" in _ && l(0, r = _.visible), "display_close_icon" in _ && l(3, m = _.display_close_icon), "close_on_esc" in _ && l(16, u = _.close_on_esc), "close_outer_click" in _ && l(4, w = _.close_outer_click), "close_message" in _ && l(5, S = _.close_message), "bg_blur" in _ && l(17, y = _.bg_blur), "width" in _ && l(18, j = _.width), "height" in _ && l(19, q = _.height), "content_width_percent" in _ && l(20, b = _.content_width_percent), "content_height_percent" in _ && l(21, g = _.content_height_percent), "content_padding" in _ && l(22, B = _.content_padding), "opacity_level" in _ && l(23, I = _.opacity_level), "gradio" in _ && l(24, d = _.gradio), "close_message_style" in _ && l(6, R = _.close_message_style), "$$scope" in _ && l(29, c = _.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*bg_blur, opacity_level*/
    8519680 && l(12, n = `
    backdrop-filter: blur(${y}px);
    -webkit-backdrop-filter: blur(${y}px);
    background-color: rgba(0, 0, 0, ${I});
    @supports not (backdrop-filter: blur(${y}px)) {
      background-color: rgba(0, 0, 0, ${I});
    }
  `), t.$$.dirty & /*width, height*/
    786432 && l(11, i = `width: ${j}px; height: ${q}px;`), t.$$.dirty & /*content_padding, content_width_percent, content_height_percent*/
    7340032 && l(10, a = (() => {
      const _ = B ? `${B}` : "0px", se = b ? `${b}%` : "100%", _e = g ? `${g}%` : "100%";
      return `width: ${se}; max-height: ${_e}; padding: ${_};`;
    })()), t.$$.dirty & /*bg_blur, opacity_level*/
    8519680 && (console.log("bg_blue", y), console.log("opacity_level", I));
  }, [
    r,
    f,
    s,
    m,
    w,
    S,
    R,
    T,
    Y,
    A,
    a,
    i,
    n,
    J,
    U,
    ie,
    u,
    y,
    j,
    q,
    b,
    g,
    B,
    I,
    d,
    o,
    ae,
    oe,
    ce,
    c
  ];
}
class n0 extends Pe {
  constructor(e) {
    super(), Ve(this, e, l0, e0, Ze, {
      elem_id: 1,
      elem_classes: 2,
      visible: 0,
      display_close_icon: 3,
      close_on_esc: 16,
      close_outer_click: 4,
      close_message: 5,
      bg_blur: 17,
      width: 18,
      height: 19,
      content_width_percent: 20,
      content_height_percent: 21,
      content_padding: 22,
      opacity_level: 23,
      gradio: 24,
      close_message_style: 6
    });
  }
}
export {
  n0 as default
};
