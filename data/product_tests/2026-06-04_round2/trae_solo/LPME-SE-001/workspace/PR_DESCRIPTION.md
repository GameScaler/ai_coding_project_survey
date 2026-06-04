## Root cause

1. `cart_total()` 先按折前小计计算运费，随后才应用折扣，导致“运费应按折后小计阶梯计算”的业务规则被破坏。
2. `apply_discount()` 对 `discount_rate` 未做边界处理：
   - 负数折扣会变相加价；
   - 大于 1 的折扣会生成负的小计，进一步影响运费/总价计算。

## Fix summary (minimal change)

- 在 `apply_discount(amount, discount_rate)` 中将 `discount_rate` clamp 到 `[0.0, 1.0]`，确保：
  - 负数折扣按 0 处理；
  - 超过 100% 的折扣按 100% 处理（小计最低为 0）。
- 在 `cart_total(items, discount_rate)` 中将运费改为基于**折后小计**计算：`shipping_fee(discounted)`。
- 保持现有 public API（函数名/签名）不变，未做无关重构。

## Verification

```bash
python3 -m unittest discover -s tests -v
```

Result: **OK (3 tests)**

## Risk notes

- 行为变更：此前允许负折扣导致“加价”，现在会被视为 0 折扣；此前允许 >1 折扣导致负小计，现在会被封顶为 1。该变更符合测试与需求，但如果上游曾依赖旧的异常行为，可能需要同步更新调用方预期。
- 浮点与四舍五入：仍按原有实现使用 `round(..., 2)`；未引入 Decimal，以避免超出“最小修复”范围。
