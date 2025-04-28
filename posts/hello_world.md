# Hello, World: the first signs of practical iO

04.28.2025 | [Sora Suegami](https://x.com/SoraSue77), [Enrico Bottazzi](https://x.com/backaes), [Pia Park](https://x.com/0xpiapark)

Today, we’re excited to announce that **we have successfully implemented [Diamond iO](https://eprint.iacr.org/2025/236)**, a straightforward construction of indistinguishability obfuscation (iO) that we published in February, and **completed its end-to-end workflow**. You can explore the codebase [here](https://github.com/MachinaIO/diamond-io). 

The current implementation includes minor differences from the theoretical construction and supports a limited range of circuit functionalities. Nonetheless, it demonstrates the concrete efficiency of the novel techniques introduced in Diamond iO, **opening a new path toward practical iO**.

## iO is powerful, but far from practical use

While technological acceleration is increasingly driven by data-centric algorithms operating on vast datasets controlled by centralized entities, there is an observable decline in individuals' control over personal data. 

We believe that a **global private computation platform** represents the only viable bridge to reconcile and further boost tech acceleration and personal data sovereignty. As the value of private information delegated to such a platform grows, it becomes necessary to rely on a security foundation that can scale regardless of the stakes involved. 

Unlike other technologies such as Multi-Party Computation (MPC) or Multi-Party Fully Homomorphic Encryption (MP-FHE), facing [privacy scalability issues](https://mirror.xyz/privacy-scaling-explorations.eth/nXUhkZ84ckZi_5mYRFCCKgkLVFAmM2ECdEFCQul2jPs), iO completely removes the perpetual reliance on committees after distributed trusted setup processes. In other words, iO unlocks a programable protocol that acts as the **perfect trustless third party**, relying solely on cryptographic hardness assumptions to guarantee the security of any secrets—akin to Nick Szabo's definition of [God Protocol](https://nakamotoinstitute.org/library/the-god-protocols/).

Following a series of studies on iO, [a breakthrough work by Aayush Jain, Huijia Lin, and Amit Sahai in 2020](https://dl.acm.org/doi/pdf/10.1145/3406325.3451093) demonstrated that iO could be constructed solely from standard assumptions, firmly established through over a decade of research. However, iO has been seen as a theoretical cryptographic primitive because of the complexity of its constructions. In fact, [one of the most recent studies on the iO implementation](https://link.springer.com/chapter/10.1007/978-3-319-15618-7_12) reports a simulation result that obfuscating a 2-bit multiplication circuit requires around 10^27 years and 20 Zetta bytes of memory.
