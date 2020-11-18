
Sharif University of Technology



Implementing Elgamal Encryption



Sina Radpour

Ali Soleimani



Course Professor:Dr. H. Peyvandi 




From November 2019 - January 2020


Elgamal Encryption System Description
As with Diffie-Hellman, the global elements of Elgamal are a prime number q and a, which is a primitive root of q. User A generates a private/public key pair as follows:
1.	Generate a random integer XA, such that 1 < XA < q – 1.
2.	Compute YA = aXA mod q.
3.	A’s private key is XA and A’s public key is {q, a, YA}.

Any user B that has access to A’s public key can encrypt a message as follows:
1.	Represent the message as an integer M in the range 0 ⩽ M ⩽ q - 1. Longer messages are sent as a sequence of blocks, with each block being an integer less than q.
2.	Choose a random integer k such that 1 ⩽ k ⩽ q – 1.
3.	Compute a one-time key K = (YA)k mod q.
4.	Encrypt M as the pair of integers (C1, C2) where C1 = ak mod q and C2 = KM mod q

User A recovers the plaintext as follows:
1.	Recover the key by computing K = (C1)XA  mod q.
2.	Compute M = (C2K -1) mod q.

Let us demonstrate why the Elgamal scheme works. First, we show how K is recovered by the decryption process:
		K = (YA)k mod q		K is defined during the encryption process
		K = (a(XA) mod q)k  mod q	substitute using YA = a(XA) mod q
		K = a(kXA) mod q		by the rules of modular arithmetic
		K = (C1 )XA mod q	           	substitute using C1 = ak mod q

Next, using K, we recover the plaintext as
		C2 = KM mod q
		(C2K-1) mod q = KMK-1 mod q = M mod q = M

Implemented Code Description
Python libraries:
We use two python libraries for implementation of ElGamal algorithm, random: for generating integer numbers and sympy: for check prime numbers.

Implementing of ElGamal Algorithm
For the security of Elgamal, we essentially want both p and the order of the subgroup q to be large primes. This means q should divide p−1. For instance, p=11 and q=5. It is typical to set p=2q+1 (that is (p−1) =2q).  When p=2q+1, they are the exact same group as Gq. This means, by using Gq, you don't have to worry about an adversary testing if certain numbers are quadratic residues or not.

	
How do we find <p,q,g>:
1.	Find a p that will have Gq: we choose a random prime q, compute p=2q+1, repeat until p is prime.
2.	Find a g that will generate Gq and not Z∗p (or any other subgroup). Since groups end with 1 and then repeat, we test if gq mod p is equal to 1. If it is, we have very likely found a generator of Gq (and very unlikely found something of order 1 or 2; we can check that g2 is not equal to 1).
3.	The description of the group is ⟨p,q,g⟩ (you could compute q from p to save space in the description).
4.	save <p,q,g> in a text file, to share it with public key.

Generating public and private keys
1.	Choose a random variable a between 2 and p-1
2.	h = ga
3.	h is Public key and a is Private key
4.	Save Public_key.txt and Private_key.txt

Encryption
1.	Need to load <p,q,g> and receiver’s public key in order to encrypt
2.	Choose a random variable r between 2 and q-1
3.	c2 (encrypted message) = multiply each character of plain text by hr  (m[i] * hr)
4.	c1 = gr
5.	return the <c1, c2> encrypted message

Decryption
1.	Need to load <p,q,g> and receiver’s private key in order to encrypt
2.	Compute c1a = c1a mod p. (a is receiver’s private key)
3.	divide each encrypted character by c1a











Implementing GUI for this project:
For making this program easier to use we decided to implement GUI. We have made this GUI with python tool for GUI named “tkinter”. GUI of this program consist of a main window and two pop-up windows which described below.
The main window consists of a textbox for getting input from user as a message for encryption or decrypted message for decryption (Figure 1). There are two buttons provided next to it. “OK” button simply gets typed message and save it as user’s message, and “Browse a file” button for browsing a text file as a message in spite of typing it. We have implemented “OK” button with tkinter button, and for browsing we used “askopenfile()” function from “Filedialog” directory. The message then will be read from the file in “read_message” function. There is also an exception handling for some situations like submitting wrong file that cannot be read or a file that is no longer accessible, which show an error message that warn the user to submit a correct file.


But in the very first step, user should provide a saving path for saving messages after encryption/decryption or keys after being automatically generated. This section has been implemented in “popup_winodw2” function in the source code of the program. User can configure saving path by press on “Saving path” button as in Figure 1. After pressing on this button a new window will appear for configuring saving location (Figure 2). User can provide the location by type it and press “Submit location” or just browse a folder by pressing on “Browse A Folder” button. We implemented generating a new window with “win=Toplevel()” that is a tkinter function for creating a new window on the top of others. We also used “askdirectory” function from File dialog directory for browsing a folder. 



After configuring saving location user should adjust keys needed for encryption/decryption. As explained in above, there are two primary keys as “Public key” and “Private key” and another three large integers as “P”, “Q”, and “G” which should be adjusted for running encryption/decryption. We implemented configuring these keys like how configuring saving location has been implemented. User can press “Configure keys” button for adjusting keys. There are five field for each of keys that user can enter values and press “Submit keys” button or just simply browse private and public key from a text file separately and browse one text file that contains all the three remaining ones (P, Q and G). Browsing from files and entering fields and button implemented as above. There is also another option for users which they can use in order to generate keys automatically by the program if they don’t have key values. There is also an exceptions handling for an error that could happen in order to submit keys that happens when user did not set saving location. In this situation an error message appears on the screen to warn user to adjust saving location first.


After all those steps explained above, user can encrypt or decrypt the message by pressing on “Encrypt” or “Decrypt” button. By pressing on them, that specific function will be called from “Elgamal” class as explained. The encrypted/decrypted button then will be saved in the path that user has been provided.
There are also some tabs that has been provided in the top of the main screen which are “File” which can be used in order to open a text file for a message, “Configure” in which user can configure keys and saving location, and “Help” which user can use to know how to use the program correctly. These tabs implemented by “Menu” class from “tkinter” and drop down menus implemented by “add_cascade” function from “Menu” class. The help window is implemented in “Help” function that create a window like described before.

