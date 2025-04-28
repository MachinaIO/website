## Future research

Our next step is to tackle the following security and efficiency challenges.

**Recent attacks on the evasive LWE assumption.** The four papers listed below—all published after the Diamond iO paper—introduce new attacks on the evasive LWE assumption. Although the security proof of Diamond iO relies heavily on this assumption, these attacks, as far as we know, succeed only for certain parameters and sampler sets that are not necessarily used in actual cryptographic schemes relying on the same assumption. We are now investigating whether any of them can be adapted to the concrete parameters and sampler employed in our construction.
- [Simple and General Counterexamples for Private-Coin Evasive LWE](https://eprint.iacr.org/2025/374.pdf)
- [Evasive LWE: Attacks, Variants & Obfustopia](https://eprint.iacr.org/2025/375.pdf)
- [Lattice-Based Post-Quantum iO from Circular Security with Random Opening Assumption](https://eprint.iacr.org/2025/390.pdf)
- [A Note on Obfuscation-based Attacks on Private-coin Evasive LWE](https://eprint.iacr.org/2025/421.pdf)

**Noise refreshing during evaluation.** As described above, we only need to support the obfuscation of a circuit that verifies a ZK proof and then decrypts the given FHE ciphertext. Nonetheless, the current implementation cannot support the obfuscation of such a circuit due to its limited input size. Specifically, since the modulus bits scale linearly due to the exponential growth of the accumulated error with respect to the input size, we are researching techniques to reduce the error during evaluation, such as one for BGG+ encodings introduced in [[HLL23]](https://eprint.iacr.org/2023/1716.pdf).


**Distributed obfuscation.** Careful reader might notice that iO is virtually worthless if the obfuscator still knows the secret inside the obfuscated program. A naive way to solve this issue is to perform the obfuscation process within an MPC but this is extremely impractical. We are excited to research more practical ways to run distributed trusted setups for obfuscation as this topic has been largely overlooked in existing literature.

## What's next?

Machina ("mah-kin-ah") iO, a project within [Privacy and Scaling Explorations (PSE)](https://pse.dev), aims to move iO from theory to practice. Alongside our research and engineering efforts, we’ll be publishing a series of posts explaining the core ideas, the vision behind the technology, and the lessons we’ve learned through implementation. If you’re interested in following our journey, we invite you to [subscribe](https://machina-io.com/subscribe.html).


## Acknowledgments

*We would like to sincerely thank the developers of [OpenFHE](https://github.com/openfheorg/openfhe-development) and [openfhe-rs](https://github.com/fairmath/openfhe-rs), open-source lattice and FHE libraries, whose optimized implementations of trapdoor sampling, RLWE primitives, and Rust bindings played a crucial role in helping us implement Diamond iO. We are also grateful to Prof. Yuriy Polyakov for his valuable advice on preimage sampling and his insightful feedback on optimizing our implementation. Any remaining errors are entirely our own responsibility.*