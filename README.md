# Register Code Generator

Generates code from SVD files.

## Installing

`pip install register-code-gen`

### Installing from source

This project uses [python-poetry](https://python-poetry.org/).  Once poetry is configured, run `poetry Install` to set up a virtual environment for this project.  Then use `poetry run register-code-gen`.

## Usage

`register-code-gen --input-file my_micro.svd`

`register-code-gen --help` for more info

## Example output

Output is unformatted.  Use [clang-format](https://clang.llvm.org/docs/ClangFormat.html) or another formatter of your choice to format the code.

### Enums

Enums are generated with documentation for field in the register that has enumerations.

```c
/**
 * Output compare 1 mode These bits define the behavior of the output reference
 * signal OC1REF from which OC1 and OC1N are derived. OC1REF is active high
 * whereas OC1 and OC1N active level depends on CC1P and CC1NP bits. Note: In
 * PWM mode, the OCREF level changes only when the result of the comparison
 * changes or when the output compare mode switches from âfrozenâ mode
 * to âPWMâ mode. Note: The OC1M[3] bit is not contiguous, located in
 * bit 16.
 */
typedef enum TIM2_oc1m1_e {
    /// Frozen - The comparison between the output compare register TIMx_CCR1
    /// and the counter TIMx_CNT has no effect on the outputs.(this mode is used
    /// to generate a timing base).
    TIM2_oc1m1_b_0x0 = 0x0,
    /// Set channel 1 to active level on match. OC1REF signal is forced high
    /// when the counter TIMx_CNT matches the capture/compare register 1
    /// (TIMx_CCR1).
    TIM2_oc1m1_b_0x1 = 0x1,
    /// Set channel 1 to inactive level on match. OC1REF signal is forced low
    /// when the counter TIMx_CNT matches the capture/compare register 1
    /// (TIMx_CCR1).
    TIM2_oc1m1_b_0x2 = 0x2,
    /// Toggle - OC1REF toggles when TIMx_CNT=TIMx_CCR1.
    TIM2_oc1m1_b_0x3 = 0x3,
    /// Force inactive level - OC1REF is forced low.
    TIM2_oc1m1_b_0x4 = 0x4,
    /// Force active level - OC1REF is forced high.
    TIM2_oc1m1_b_0x5 = 0x5,
    /// PWM mode 1 - In upcounting, channel 1 is active as long as
    /// TIMx_CNT<TIMx_CCR1 else inactive. In downcounting, channel 1 is inactive
    /// (OC1REF='0) as long as TIMx_CNT>TIMx_CCR1 else active (OC1REF=1).
    TIM2_oc1m1_b_0x6 = 0x6,
    /// PWM mode 2 - In upcounting, channel 1 is inactive as long as
    /// TIMx_CNT<TIMx_CCR1 else active. In downcounting, channel 1 is active as
    /// long as TIMx_CNT>TIMx_CCR1 else inactive.
    TIM2_oc1m1_b_0x7 = 0x7,
    /// Retriggerable OPM mode 1 - In up-counting mode, the channel is active
    /// until a trigger event is detected (on TRGI signal). Then, a comparison
    /// is performed as in PWM mode 1 and the channels becomes inactive again at
    /// the next update. In down-counting mode, the channel is inactive until a
    /// trigger event is detected (on TRGI signal). Then, a comparison is
    /// performed as in PWM mode 1 and the channels becomes inactive again at
    /// the next update.
    TIM2_oc1m1_b_0x8 = 0x8,
    /// Retriggerable OPM mode 2 - In up-counting mode, the channel is inactive
    /// until a trigger event is detected (on TRGI signal). Then, a comparison
    /// is performed as in PWM mode 2 and the channels becomes inactive again at
    /// the next update. In down-counting mode, the channel is active until a
    /// trigger event is detected (on TRGI signal). Then, a comparison is
    /// performed as in PWM mode 1 and the channels becomes active again at the
    /// next update.
    TIM2_oc1m1_b_0x9 = 0x9,
    /// Combined PWM mode 1 - OC1REF has the same behavior as in PWM mode 1.
    /// OC1REFC is the logical OR between OC1REF and OC2REF.
    TIM2_oc1m1_b_0xc = 0xC,
    /// Combined PWM mode 2 - OC1REF has the same behavior as in PWM mode 2.
    /// OC1REFC is the logical AND between OC1REF and OC2REF.
    TIM2_oc1m1_b_0xd = 0xD,
    /// Asymmetric PWM mode 1 - OC1REF has the same behavior as in PWM mode 1.
    /// OC1REFC outputs OC1REF when the counter is counting up, OC2REF when it
    /// is counting down.
    TIM2_oc1m1_b_0xe = 0xE,
    /// Asymmetric PWM mode 2 - OC1REF has the same behavior as in PWM mode 2.
    /// OC1REFC outputs OC1REF when the counter is counting up, OC2REF when it
    /// is counting down.
    TIM2_oc1m1_b_0xf = 0xF,
} TIM2_oc1m1_t;
```

### Registers

Registers use enum types to help make documentation for the register and the field easier to access in most IDEs.

```c
/**
 * capture/compare mode register 1 (output mode)
 */
typedef union TIM2_ccmr1_output_u {
    struct {
        /// Capture/Compare 1 selection This bit-field defines the direction of
        /// the channel (input/output) as well as the used input. Note: CC1S
        /// bits are writable only when the channel is OFF (CC1E = 0 in
        /// TIMx_CCER).
        TIM2_cc1s_t cc1s : 2;
        /// Output compare 1 fast enable
        uint32_t oc1fe : 1;
        /// Output compare 1 preload enable Note: The PWM mode can be used
        /// without validating the preload register only in one-pulse mode (OPM
        /// bit set in TIMx_CR1 register). Else the behavior is not guaranteed.
        TIM2_oc1pe_t oc1pe : 1;
        /// Output compare 1 mode These bits define the behavior of the output
        /// reference signal OC1REF from which OC1 and OC1N are derived. OC1REF
        /// is active high whereas OC1 and OC1N active level depends on CC1P and
        /// CC1NP bits. Note: In PWM mode, the OCREF level changes only when the
        /// result of the comparison changes or when the output compare mode
        /// switches from âfrozenâ mode to âPWMâ mode. Note: The
        /// OC1M[3] bit is not contiguous, located in bit 16.
        TIM2_oc1m1_t oc1m1 : 3;
        /// Output compare 1 clear enable
        TIM2_oc1ce_t oc1ce : 1;
        /// Capture/compare 2 selection This bit-field defines the direction of
        /// the channel (input/output) as well as the used input. Note: CC2S
        /// bits are writable only when the channel is OFF (CC2E = 0 in
        /// TIMx_CCER).
        TIM2_cc2s_t cc2s : 2;
        /// Output compare 2 fast enable
        uint32_t oc2fe : 1;
        /// Output compare 2 preload enable
        uint32_t oc2pe : 1;
        /// Output compare 2 mode
        uint32_t oc2m : 3;
        /// Output compare 2 clear enable
        uint32_t oc2ce : 1;
        /// Output Compare 1 mode - bit 3
        uint32_t       oc1m_3 : 1;
        uint32_t const reserved_17 : 7;
        /// Output Compare 2 mode - bit 3
        uint32_t oc2m_3 : 1;
    };
    uint32_t bits;
} TIM2_ccmr1_output_t;
STATIC_ASSERT_TYPE_SIZE(TIM2_ccmr1_output_t, sizeof(uint32_t));
```

Note: Some fields could be split up in a register.  For example, `oc1m1` and `oc1m_3` both map back to `TIM2_oc1m1_t`.  In an application you may need to do something like this:

```c
STM_TIM1->ccmr1_output.oc1m_3 = TIM1_oc1m2_b_0x6 >> 3;
STM_TIM1->ccmr1_output.oc1m1  = TIM1_oc1m1_b_0x6;
```

### Peripheral

Generate a structure for each peripheral.  Register-code-generator produces a union when a register has two or more different modes of access.  For example, when this timer is in input compare vs output compare modes.

```c
/**
 * General-purpose-timers
 */
typedef struct TIM2_peripheral_registers_s {
    /// control register 1
    TIM2_cr1_t cr1;
    /// control register 2
    TIM2_cr2_t cr2;
    /// slave mode control register
    TIM2_smcr_t smcr;
    /// DMA/Interrupt enable register
    TIM2_dier_t dier;
    /// status register
    TIM2_sr_t sr;
    /// event generation register
    TIM2_egr_t egr;
    union {
        /// capture/compare mode register 1 (input mode)
        TIM2_ccmr1_input_t ccmr1_input;
        /// capture/compare mode register 1 (output mode)
        TIM2_ccmr1_output_t ccmr1_output;
    };
    union {
        /// capture/compare mode register 2 (input mode)
        TIM2_ccmr2_input_t ccmr2_input;
        /// capture/compare mode register 2 (output mode)
        TIM2_ccmr2_output_t ccmr2_output;
    };
    /// capture/compare enable register
    TIM2_ccer_t ccer;
    union {
        /// counter
        TIM2_cnt_t cnt;
        /// counter
        TIM2_cnt_alternate5_t cnt_alternate5;
    };
    /// prescaler
    TIM2_psc_t psc;
    /// auto-reload register
    TIM2_arr_t    arr;
    uint8_t const reserved_0x30[4];
    /// capture/compare register 1
    TIM2_ccr1_t ccr1;
    /// capture/compare register 2
    TIM2_ccr2_t ccr2;
    /// capture/compare register 3
    TIM2_ccr3_t ccr3;
    /// capture/compare register 4
    TIM2_ccr4_t   ccr4;
    uint8_t const reserved_0x44[4];
    /// DMA control register
    TIM2_dcr_t dcr;
    /// DMA address for full transfer
    TIM2_dmar_t dmar;
    /// TIM option register
    TIM2_or1_t    or1;
    uint8_t const reserved_0x54[12];
    /// TIM alternate function option register 1
    TIM2_af1_t    af1;
    uint8_t const reserved_0x64[4];
    /// TIM alternate function option register 1
    TIM2_tisel_t tisel;
} TIM2_peripheral_registers_t;
```
