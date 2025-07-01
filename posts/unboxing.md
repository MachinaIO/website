---
title: iO from a new perspective

---

# Unboxing iO: building from familiar crypto blocks

> This article is written by @letargicus with review of @SoraSuegami and @piapark and proofreading from LLM

### Introduction

<!-- During Devcon 2024 I heard for the first time about iO thanks to a [presentation](https://youtu.be/5hDj0TB8s18?si=5bBDZYINaFnxTip2) by Barry Whitehat. Leaving the room, I feel fascinated by the affordances of such a technology but also confused about its nature. How does this mysterious and incredibly powerful cryptographic technique look like under the hood? What are its core components? What primitives does it rely on? -->

<!-- In the following months of learning, studying and implementing iO I realized that the existing resources are either super advanced and intimidating academic papers or "for-newbies" articles that only tells you what iO can enable but nothing about how to construct it. It seems that no one ever tried to describe iO using building blocks that are more familiar to me. The goal of this article is to provide such new and missing perspective. -->

<!-- 
To do so, we will take a non-interactive conditional signature printer as motivating example and iteratively try to build it using familiar technologies. More specifically, we will define functional encryption (FE), derive iO as an augmeneted version of FE, and use it to build such rather dummy application. We will then smoothly extend the utility of iO to build something more meaningful: encrypted smart contracts. By the end of the article, the reader will be convinced by the power of iO and be provided with a map that defines all the theoretical building blocks required to learn and construct iO. -->

Over the past few months of researching and implementing indistinguishability obfuscation (iO), we’ve noticed a frustrating gap in the available resources. Most papers are highly technical and intimidating, while beginner friendly articles stay at a vague, feature level overview: they tell you what iO can enable but nothing about how to construct it.

This article aims to bridge that gap. We’ll work through a concrete, end to end example, of a non-interactive conditional signature printer, building it in several attempts **using familiar cryptographic primitives as building blocks**. By the end, you should have a clear roadmap of the theoretical building blocks behind iO and a hands on understanding of its power.

<!-- ### Goal: Non-interactive conditional signature printer

The goal is to build non-interactive conditional signature program defined as follows:

$$
f(k, x) =
\begin{cases}
\textsf{sign}(k, x) & \text{if } x \text{ is prime}\\
\perp & \text{otherwise}.
\end{cases}
$$

Meaning, program $f$ is returning signature for message $x$ that signed by key $k$ if only $x$ is prime number. Otherwise it doesn't returns.

The program involves a key owner, who generates a program and holds a signing key $k$, and a set of users, potentially unknown by the key owner, who provide an numbers $x$ as input and conditionally obtain a signature. 

Also the program involves two requirement. First, a user should be able to conditionally obtain a valid signature **without interacting with the key owner**. Even if the key owner goes on-holiday on a lost island, the user should still be able to (conditionally) obtain a signature. Second, **no information related to the signing key should be leaked** to the user beyond $f(k, x)$. So, publishing the program source code is not a valid solution because it leaks the signing key $k$. 

Then how can we build this program by satisfying two requirements above?
 -->
### Goal: Non-Interactive Conditional Signature Printer

Our target program $f$ behaves as follows:

$$
f(k, x)=
\begin{cases}
\textsf{sign}(k, x) & \text{if } x \text{ is prime},\\
\bot & \text{otherwise}.
\end{cases}
$$

That is, given a message $x$, it outputs a valid signature under the secret key $k$ when $x$ is prime, and $\bot$ otherwise. 

The setting involves a **key owner**, who generates the program and holds the signing key $k$, and a collection of **users**, who supply numbers $x$ and hope to obtain signatures when the condition holds. Any viable construction must meet two requirements:

1. **No interaction.** Once the program is published, users must be able to run it and (conditionally) obtain signatures without ever contacting the key owner. Even if the key owner is off-grid on a desert island, the system must keep working.
2. **Key privacy.** Executing the program should reveal nothing about $k$ beyond what is already implicit in the output $f(k, x)$. Simply releasing the source code is therefore out of the question, because it would expose the key.

In the sections that follow we’ll try to build this program with various attempts: first with a public-lookup, then with fully homomorphic encryption (FHE), next with functional encryption (FE), and finally with an augmented version of FE that we'll call indistinguishability obfuscation (iO). 


<!-- ### Attempt #1 - public lookup table

The most immediate solution that one can think about is to allow the key owner, given the signing key $k$, to publish a truth table that associates every possible user input $x_i$ with the corresponding output $f(k,x_i)$. In particular, the key owner must fix an input domain, let's say 64 bits, and compute the function $f(k,x_i)$ for each of the $2^{64}$ possible input combinations. And you could imagine truth table as a large mapping of all possible $x_i$ as a key and look up value $f(k,x_i)$. 

While this solution satisfies the two requirements defined in the previous paragraph, we also notice that it scales exponentially to the input bit size and won't therefore be practical in any real world application. Therefore, we additionally require the work of the evaluator to not be exponentional to the user's input bit size.

-->

### Attempt #1 – Public truth table

We start from something straightforward: let the key owner, holding the signing key $k$, publish a truth table that maps every possible input $x_i$ to the corresponding output $f(k,x_i)$. Concretely, the key owner fixes an input domain, say 64 bits, and precomputes $f(k,x_i)$ for each of the $2^{64}$ possible inputs. You can imagine the truth table as a huge dictionary keyed by every $x_i$, with each value equal to $f(k,x_i)$. Given Alice as user with input $x=7$, she could lookup the trust table corresponding to her key and obtain $f(k, 7)$.

While this approach satisfies the two requirements laid out earlier, it scales exponentially with the input size, so it's impractical. We therefore add a third requirement: the work done by the evaluator should not grow exponentially with the bit length of the user’s input.


### Attempt #2 - fully homomorphic encryption

As you might have heard in some conference, fully homomorphic encryption (FHE) is always mentioned with respect to "computation on encrypted data", so it sounds a potential solution to our problem.

We first list the core APIs of FHE. In particular, we describe the secret key variant. I won't go too deep into this as, differently from iO, you can find plenty of [great resources online](https://fhe.org/resources/). 

$\mathsf{FHE.Keygen}() \rightarrow sk$
$\mathsf{FHE.Enc}(k, sk) \rightarrow ct_k$
$\mathsf{FHE.Eval}(f, ct_k) \rightarrow ct_{f(k)}$
$\mathsf{FHE.Dec}(ct_{f(k)}, sk) \rightarrow f(k)$

Here's a sketch of a non-interactive conditional signature printer based on FHE. The key owner is also the holder of the FHE secret key $sk$. The role of the cloud is to store data produced by the key owner and make them accessible to everyone, including any other user such as Bob or Carl that might be unknown to the key owner.

![FHE](https://hackmd.io/_uploads/HyIN1bkVxg.png)

Although Alice can evaluate the function $f$ over the encrypted signing key $ct_k$ and her input $7$ to obtain an encrypted version of the output $ct_{f(k,7)}$, this still requires a further interaction with key owner to decrypt it. So this violates our no-interaction requirement. On the other hand, publishing the FHE secret key $sk$ would allow for non-interactive decryption but also violate the security requirement of our application, since now Alice can also decrypt $ct_k$. We need to think deeper...

<!-- title FHE-based effort
actor key owner
fontawesome6solid f0c2 Cloud
actor Alice
key owner->key owner: Enc(k, sk) = ct_k
key owner->Cloud: ct_k
Cloud->Alice: ct_k
Alice->Alice:Eval(f, ct_k, 7)\n= ct_f(k, 7)
Alice->key owner: ct_f(k, 7)
key owner->key owner: Dec(ct_f(k, 7), sk) \n= f(k, 7)
key owner->Alice:f(k, 7) -->

### Attempt #3 - functional encryption

The next technology that we are going to introduce is functional encryption (FE). This is a less "popular" cryptographic building block. This is not surprising since it took me many months to find a valid motivating application for it. We first analyse the core APIs of FE and describe such application. Only then we'll be equipped to apply FE to our problem.

$\mathsf{FE.Setup}() \rightarrow mpk, msk$
$\mathsf{FE.Keygen}(msk, f) \rightarrow sk_f$
$\mathsf{FE.Enc}(k, mpk) \rightarrow ct_k$
$\mathsf{FE.Dec}(ct_k, sk_f) \rightarrow f(k)$

The motivating example I chose to help you understand FE is email spam filtering: on one hand, Daisy doesn't want to rely on a cloud mail provider able to read all her emails. On the other hand, a secure (fully encrypted) cloud mail provider wouldn't be able to detect spam emails and require Daisy to download each email, including potentiall spam ones, consuming her precious bandwidth and device space. 

Instead, Daisy can run the setup to obtain a master public key $mpk$ and a master secret key $msk$. Use the latter to generate a functional secret key $sk_f$ tied to a function $f$ that detects if an email is spam (returns $1$) or not (returns $0$). Share the functional key with her secure email cloud provider. Every sender can encrypt an email $k$ directed to Daisy under her master public key $mpk$ and share the ciphertext $ct_k$ to the email provider. For each email received by Daisy, the provider can run the FE decryption and learn whether an email is spam or not and only serve the non-spam ones to Daisy. More importantly, the server doesn't learn any information about the content of an email beyond whether this is spam or not. We additionally note that the function $f$ is public to the receiver of $sk_f$. 

Having clarified the interface of FE, we can go back to our problem: building a non-interactive conditional signature printer. Here's a potential sketch.

![FE](https://hackmd.io/_uploads/Bk-ad-1Egg.png)

While we appreciate the non-interactive property of FE decryption we still have a major issue. FE decryption doesn't allow Alice to additionally inject their input $x=7$. How can the key owner allow for the inputs dynamically chosen by Alice (and, potentially, by many other unknown users)? A naive solution is for the key owner to generate a functional key for any possible input combination. Specifically, for each possible input $x_i$ the key owner defines a function $f_{[x_i]}(k)$ that, on input $k$ returns $f(k, x_i)$ where $x_i$ is hardcoded into the function definition. In that scenario, Alice could use the functional key for $f_{[7]}(k)$ and obtain the decrypted value $f(k, 7)$. But this means that the work of the key owner is exponential to the number of input bits. Are we back to square one? Rather than discouraging ourselves, we see the glass half full: we finally found a way to allow for non-interactive decryption binded to a specific function set by the key owner. We just need to add a little piece to it... 

<!-- title FE-based effort
actor key owner
fontawesome6solid f0c2 Cloud
actor Alice
key owner->key owner: Enc(k, mpk) = ct_k \nKeyGen(msk, f) = sk_f
key owner->Cloud: ct_k, sk_f
Cloud->Alice: ct_k, sk_f
Alice->Alice:Dec(sk_f, ct_k)= f(k, 7) -->

### Attempt #4 Augmented FE a.k.a. iO

We now imagine a wishful solution: what if the scheme supported an additional API (in blue) that allows Alice to extend the ciphertext provided by the key owner with her dinamically chosen input $x$.

$\mathsf{FE.Setup}() \rightarrow mpk, msk$
$\mathsf{FE.Keygen}(msk, f) \rightarrow sk_f$
$\mathsf{FE.Enc}(k, mpk) \rightarrow ct_k$
<font color="#1936C9">$\mathsf{FE.ExtendCT}(ct_k, x) \rightarrow ct_{k || x}$</font>
$\mathsf{FE.Dec}(ct_{k || x}, sk_f) \rightarrow f(k, x)$

Here's the sketch of the application assuming this augemented FE construction

![A_FE](https://hackmd.io/_uploads/ryK9AbJVxx.png)

<!-- title Augmented FE-based effort
actor key owner
fontawesome6solid f0c2 Cloud
actor Alice
key owner->key owner: Enc(k, mpk) = ct_k \nKeyGen(msk, f) = sk_f
key owner->Cloud: ct_k, sk_f
Cloud->Alice: ct_k, sk_f
Alice->Alice:ExtendCT(ct_k, x) = ct_k,x \n Dec(sk_f, ct_k,x)= f(k, 7) -->

Success! This solution satisfies all the required properties:

- Alice, and potentially any other user, can obtain the result of $f(k, x)$ without any interaction with the key owner
- The construction is secure as the users nothing more than $f(k, x)$. The definition of $f$ is public but this is not an issue
- No exponential effort is required from the key owner 

Before moving forward, we do notice that our interface has become too cluttered and, while cleaning it up, we redefine it as iO!

$$
\begin{aligned}
  % ---------- first group ----------
  \left.
    \begin{array}{l}
      \mathsf{FE.Setup}() \rightarrow mpk, msk\\
      \mathsf{FE.Keygen}(msk, f) \rightarrow sk_f\\
      \mathsf{FE.Enc}(k, mpk) \rightarrow ct_k
    \end{array}
  \right\} &\;\mathsf{iO.Obf}(f(k,\cdot)) \rightarrow \tilde{C}
  \\[8pt]
  % ---------- second group ----------
  \left.
    \begin{array}{l}
      \mathsf{FE.ExtendCT}(ct_k, x) \rightarrow ct_{k \,\|\, x}\\
      \mathsf{FE.Dec}(ct_{k \,\|\, x}, sk_f) \rightarrow f(k, x)
    \end{array}
  \right\} &\;\mathsf{iO.Eval}(\tilde{C}, x) \leftarrow f(k, x)
\end{aligned}
$$

Everything (hopefully) became much cleaner now. iO can be viewed as an extended version of FE that allows a user to inject their inputs bits into the ciphertext. The interface is set to allow an obfuscator (which, in our example, is the key owner) to set a public function $f$ that takes as inputs a secret $k$ and another yet unknown input of fixed size and obtain an obfuscated version $\tilde{C}$ of that program. The obfuscated program can be freely published to the public and any evaluator (such as Alice) with input $x$ can evaluate it to obtain $f(k, x)$.

<!-- title iO-based effort
actor key owner
fontawesome6solid f0c2 Cloud
actor Alice
key owner->key owner: Obf(f(k, -)) = C~
key owner->Cloud:C~
Cloud->Alice: C~
Alice->Alice:Eval(C~, x) = f(k, x) -->

The final sketch for our non-interactive conditional signature printer build via iO looks as follows:

![IO](https://hackmd.io/_uploads/B1u0Gf1Elg.png)


This is exactly the process we followed to build [Diamond iO](https://eprint.iacr.org/2025/236). We started from an existing FE scheme, namely [[AKY24a]](https://eprint.iacr.org/archive/2024/1719/20241022:040259) and figure out a way to allow an evaluator to extend the ciphertext by inserting their dynamically chosen input bits without requiring exponential effort.

The following diagram illustrates the program that we have been manage to obfuscate. In particular, everything that is inside the dotted rectangle represents our obfuscated program $\tilde{C}$:
- the function defintion $f$, made of the set of arithmetic gates to be performed by the program, is public
- the signing key $k$ is private

![Screenshot 2025-06-21 at 10.45.44](https://hackmd.io/_uploads/SJlUSWg4Egg.png)

<!-- ### Extension to encrypted smart contracts

We now move our focus to build encrypted smart contracts. These are smart contracts that enjoy all the properties of current ones while keeping their state private.

![Screenshot 2025-06-28 at 16.10.39](https://hackmd.io/_uploads/SkQsLgCEle.png)
Slide from a recent Vitalik's presentation

We take private voting as the motivating example to justify the need for encrypted smart contracts. Our private voting app requires that:

- The voting period lasts until block $t$
- Individual votes ($1$ or $0$) should always remain secret 
- After block $t$, the final result of the election, whether there were more $1$s or $0$s, is revealed (note that this shouldn't reveal any information about the winning margin or the vote distribution)

We notice that this is different from the more traditional private voting app, in which only privacy the voter's identity is required. I encourage the reader to stop for a second and think about the differences about the two application and why the former cannot be built solely with zk ([hint](https://www.leku.blog/beyond-zkml/)).


Encrypted smart contracts can already be built today with FHE and, specifically, with a [FHEvm](https://github.com/zama-ai/fhevm/blob/main/fhevm-whitepaper-v2.pdf). In such scenario a private smart contract is designed as follows:

- Holds its state in an encrypted format, specifically as ciphertexts encrypted under (public-key) FHE. All the states are required to be encrypted under the same key to guarantee interoperability
- Sets state transition functions as a FHE evaluation functions
- Sets decryption rules: what can be decrypted, when and by whom

We can therefore design our private voting app as follows:

- The state is represented by the encrypted (partial) election result
- The voting state transition takes an encrypted vote and homomorphically updates the partial election result 
- The decryption rule is set such that everyone can decrypt the state (and the state only) when block $t$ is reached

The biggest limitation of such architecture relies in the same limitation of FHE what we identified in our attempt #2: someone has to hold the decryption key! Obviously outsourcing the ownership of such key to a single trusted party is not a wise solution as this party can potentially decrypt any private state. A better solution, as suggested in the FHEvm whitepaper, is to split the decryption key across a committee of $n$ parties where only a subset $t$ of them is necessary to recover the whole decryption key. Users of the fhEVM can broadcast decryption requests to this committee and obtain the decryption results after having convinced at least $t$ members that their request is legit. The risk is that committee members collude and decrypt states despite the decryption rules set inside the smart contract. Or asseble the decryption key and sell it to an adversary. As an example, $t$ of the committee member could meet in a room, reasseble the decryption key, and decrypt the whole blockchain. More worringly, they could do so while going undetected: there's no mechanism in place to catch any potential misbehaviour of committee members (although there exists some [reserarch effort](https://eprint.iacr.org/2023/1724) to this direction).

We build a solution to this problem based on iO. In particular, the architecture of the application remains largely the same. We only want to get rid of the committee for decryption. We do so by replacing it with a **conditional and non-interactive decryptor**.

We construct this by obfusacting a program takes as input a ciphertext $ct_y$ and a blockchain consensus proof $\pi$. Such proof is designed to attest that there is a valid (signed by the validators) blockchain state in which $ct_y$ is allowed to be decrypted. The program verifies the proof and conditionally decrypt the ciphertext, with the decryption key $k$. More importantly, because of the obfuscation properties, the decryption key $k$ is not revealed by $\tilde{C}$.

In the updated version of the FHEvm that relies on iO, users can non-interactively decrypt states by evaluating the obfuscated program over their inputs. No reliance on a committee means no collusion risk! Obviously, any attempt to decrypt some ciphertext that is not meant to be accessed will fail as this would require a consensus proof from an invalid state. If we build this FHEvm on Ethereum, obtaining such proof is impossible to obtain unless a large portion of Ethereum validators maliciously collude. 

Are we done? The careful reader might have noticed a limit in our definition of iO. The obfuscation step is performed by a single part that holds the value $k$. In the context of encrypted smart contracts, this means that there is a part that holds the decryption key at a moment in time and can, potentially, maliciously use it to decrypt states at any moment in time after the obfuscated circuit is generated. To solve for this problem, we propose a setup in which the obfuscation is designed as a distributed process in which any party can jump in and inject some randomness. Similarly to a zk trusted setup, as long as a one party out of the $n$ parties joining the ceremony gets rid of their randomness, the security of the construction is safe and no-one can reconstruct the private input $k$. We highlight that, altough thoretically possible, there's no existing concretely efficient solution to this problem in academia.

![io_zuBerlin.001](https://hackmd.io/_uploads/rkxSQ-44lg.jpg)
![io_zuBerlin.002](https://hackmd.io/_uploads/B1-BQbV4le.jpg)
 -->
 
### Final Building Blocks

We saw the iO is required to build a non-interactive conditional signature printer and it can be viewed as an extended version of FE that supports ciphertext re-use. Now we can finally sketch out a map of the core primitives needed to reach iO, with pointers to the main academic references.

<!-- If we are able to build a non-interactive conditional signature printer, we can also build a conditional FHE decryptor and achieve trustless encrypted smart contracts.  -->

![Screenshot 2025-07-01 at 13.35.47](https://hackmd.io/_uploads/Syb38abreg.png)

To build functional encryption, we heavily rely on the construction introduced by [[AKY24a]](https://eprint.iacr.org/archive/2024/1719/20241022:040259) which only uses matrix multiplication, [BGG+ encoding](https://www.youtube.com/watch?v=O0NoW4UOd9Y) and [lattice trapdoors](https://eprint.iacr.org/2011/501). Once functional encryption is built, there are existing transformation to iO, they all rely on the concept of extending FE to allow the evaluator to dynamically insert their input bits inside the FE ciphertext. Constructions from [[AKY24b]](https://eprint.iacr.org/2024/1720) and [[AJ15]](https://www.youtube.com/watch?v=4TR_NCSqG4I&t=321s) obtain iO via a recursive usage of FE that represents the main efficiency bottleneck of current iO constructions. Conversely, our construction [[SBP25]](https://eprint.iacr.org/2025/236) buils iO from FE using [AKY24a] in a non-black-box way allowing us to obtain a structure that replaces recursive FE with simple matrix multiplications.

### Conclusion

Throughout the sections, we’ve taken a look at various ways to construct a non-interactive conditional signature printer. Among these attempts, the iO based construction is the only one that strictly satisfies our requirements. Although [we still need to push for its practicality first](https://machina-io.com/posts/hello_world_first.html), we believe iO could unlock applications that were impossible before. We hope you’re as excited as we are about the future possibilities of this technology!
