package twisted.util;

/**
  * Implements the Unix crypt function in java.
  * Unfunkified and made into a standalone class by James Knight (jknight@ai.mit.edu)
  * Originally by John F. Dumas (jdumas@zgs.com), Raif Naffah, David Hopwood
  *	  Copyright 1995-1997 <a href="http://www.systemics.com/">Systemics Ltd</a>
  * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 
  *	 1. Redistributions of source code must retain the copyright notice, this list of conditions and the following disclaimer. 
  *	 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
  *	 3. All advertising materials mentioning features or use of this software must display the following acknowledgement: This product includes software developed by the Cryptix Development Team (http://www.systemics.com/docs/cryptix/) 
  * THIS SOFTWARE IS PROVIDED BY SYSTEMICS LTD ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
*/

public class UnixCrypt
{

// Variables and constants
//...........................................................................


	private static final int
		ROUNDS = 16,						// number of encryption/decryption rounds
		KEY_LENGTH = 8,						// DES key length in bytes
		INTERNAL_KEY_LENGTH = 32;			// number of elements in key schedule

	private static final int[] SKB = new int[8 * 64];		// blank final
	private static final int SP_TRANS[] = new int[8 * 64];	// blank final

	static {
		//
		// build the SKB table
		//
		
		// represent the bit number that each permutated bit is derived from
		// according to FIPS-46
		String cd =
			"D]PKESYM`UBJ\\@RXA`I[T`HC`LZQ"+"\\PB]TL`[C`JQ@Y`HSXDUIZRAM`EK";
		int j, s, bit;
		int count = 0;
		int offset = 0;
		for (int i = 0; i < cd.length(); i++) {
			s = cd.charAt(i) - '@';
			if (s != 32) {
				bit = 1 << count++;
				for (j = 0; j < 64; j++)
					if ((bit & j) != 0) SKB[offset + j] |= 1 << s;
				if (count == 6) {
					offset += 64;
					count = 0;
				}
			}
		}

		//
		// build the SP_TRANS table
		//
		
		// I'd _really_ like to just say 'SP_TRANS = { ... }', but
		// that would be terribly inefficient (code size + time). 
		// Instead we use a compressed representation --GK
		String spt =
			"g3H821:80:H03BA0@N1290BAA88::3112aIH8:8282@0@AH0:1W3A8P810@22;22"+
			"A18^@9H9@129:<8@822`?:@0@8PH2H81A19:G1@03403A0B1;:0@1g192:@919AA"+
			"0A109:W21492H@0051919811:215011139883942N8::3112A2:31981jM118::A"+
			"101@I88:1aN0<@030128:X;811`920:;H0310D1033@W980:8A4@804A3803o1A2"+
			"021B2:@1AH023GA:8:@81@@12092B:098042P@:0:A0HA9>1;289:@1804:40Ph="+
			"1:H0I0HP0408024bC9P8@I808A;@0@0PnH0::8:19J@818:@iF0398:8A9H0<13@"+
			"001@11<8;@82B01P0a2989B:0AY0912889bD0A1@B1A0A0AB033O91182440A9P8"+
			"@I80n@1I03@1J828212A`A8:12B1@19A9@9@8^B:0@H00<82AB030bB840821Q:8"+
			"310A302102::A1::20A1;8"; // OK, try to type _that_!
			// [526 chars, 3156 bits]
		// The theory is that each bit position in each int of SP_TRANS is
		// set in exactly 32 entries. We keep track of set bits.
		offset = 0;
		int k, c, param;
		for (int i = 0; i < 32; i++) { // each bit position
			k = -1; // pretend the -1th bit was set
			bit = 1 << i;
			for (j = 0; j < 32; j++) { // each set bit
				// Each character consists of two three-bit values:
				c = spt.charAt(offset >> 1) - '0' >> (offset & 1) * 3 & 7;
				offset++;
				if (c < 5) {
					// values 0...4 indicate a set bit 1...5 positions
					// from the previous set bit
					k += c + 1;
					SP_TRANS[k] |= bit;
					continue;
				}
				// other values take at least an additional parameter:
				// the next value in the sequence.
				param = spt.charAt(offset >> 1) - '0' >> (offset & 1) * 3 & 7;
				offset++;
				if (c == 5) {
					// indicates a bit set param+6 positions from
					// the previous set bit
					k += param + 6;
					SP_TRANS[k] |= bit;
				} else if (c == 6) {
					// indicates a bit set (param * 64) + 1 positions
					// from the previous set bit
					k += (param << 6) + 1;
					SP_TRANS[k] |= bit;
				} else {
					// indicates that we should skip (param * 64) positions,
					// then process the next value which will be in the range
					// 0...4.
					k += param << 6;
					j--;
				}
			}
		}
	}

	private static final byte[] CON_SALT = {
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
		0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 
		0x0A, 0x0B, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 
		0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 
		0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 
		0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 
		0x23, 0x24, 0x25, 0x20, 0x21, 0x22, 0x23, 0x24, 
		0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 
		0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 
		0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 
		0x3D, 0x3E, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00};

	private static final char[] COV_2CHAR = {
		0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 
		0x36, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 
		0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 
		0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 
		0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x61, 0x62, 
		0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 
		0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 
		0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A};

	/**
	 * Hashes the password with the salt the same way Unix's crypt() function does.
	 *
	 * @param original	the password
	 * @param salt the two character salt to use.
	 * @return the hashed password
	 */
	public static String crypt(String original, String salt) {
		int i, j;
		char salt0, salt1;
 
		if (salt == null)
			salt = "";
		salt += "AA";
		salt0 = (char) (salt.charAt(0) & 0x7F);
		salt1 = (char) (salt.charAt(1) & 0x7F);

		byte[] key = new byte[8];
		for (i = 0; i < key.length && i < original.length(); i++)
		{
			int b;
			b = (byte)original.charAt(i) << 1;
			key[i] =   (byte)(b |
							   (((b >> 1) ^
								(b >> 2) ^
								(b >> 3) ^
								(b >> 4) ^
								(b >> 5) ^
								(b >> 6) ^
								(b >> 7)) & 0x01));
		}

		int sKey[] = makeKey(key);
		int[] out =
			crypt3(sKey, CON_SALT[salt0] & 0xFF, (CON_SALT[salt1] & 0xFF) << 4);

		i = out[0];
		j = out[1];

		byte[] b = {
			(byte) i, (byte)(i >>> 8), (byte)(i >>> 16), (byte)(i >>> 24),
			(byte) j, (byte)(j >>> 8), (byte)(j >>> 16), (byte)(j >>> 24),
			0};
		int y = 0;
		int u = 0x80;
		int c;

		char[] buffer = new char[13];

		i = 0;
		buffer[i++] = salt0;
		buffer[i++] = salt1;
		while (i < buffer.length) {
			for (j = 0, c = 0; j < 6; j++) {
				c <<= 1;
				if (((int) b[y] & u) != 0)
					c |= 1;
				u >>>= 1;
				if (u == 0) {
					y++;
					u = 0x80;
				}
			}
			buffer[i++] = COV_2CHAR[c];
		}
		return new String(buffer);
	}

	/**
	 * Expands a user-key to a working key schedule.
	 *
	 * @param  key	the user-key object to use.
	 */
	private static int[] makeKey (byte[] userkey)
	{
		int[] sKey = new int[INTERNAL_KEY_LENGTH];

/*		  if (userkey == null)
			throw new InvalidKeyException(getAlgorithm() + ": Null user key");

		if (userkey.length != KEY_LENGTH)
			throw new InvalidKeyException(getAlgorithm() + ": Invalid user key length");
*/
		int i = 0;
		int c = (userkey[i++] & 0xFF)		|
				(userkey[i++] & 0xFF) <<  8 |
				(userkey[i++] & 0xFF) << 16 |
				(userkey[i++] & 0xFF) << 24;
		int d = (userkey[i++] & 0xFF)		|
				(userkey[i++] & 0xFF) <<  8 |
				(userkey[i++] & 0xFF) << 16 |
				(userkey[i++] & 0xFF) << 24;

		int t = ((d >>> 4) ^ c) & 0x0F0F0F0F;
		c ^= t;
		d ^= t << 4;
		t = ((c << 18) ^ c) & 0xCCCC0000;
		c ^= t ^ t >>> 18;		  
		t = ((d << 18) ^ d) & 0xCCCC0000;
		d ^= t ^ t >>> 18;		  
		t = ((d >>> 1) ^ c) & 0x55555555;
		c ^= t;
		d ^= t << 1;
		t = ((c >>> 8) ^ d) & 0x00FF00FF;
		d ^= t;
		c ^= t << 8;
		t = ((d >>> 1) ^ c) & 0x55555555;
		c ^= t;
		d ^= t << 1;

		d = (d & 0x000000FF) <<	 16 |
			(d & 0x0000FF00)		|
			(d & 0x00FF0000) >>> 16 |
			(c & 0xF0000000) >>>  4;
		c &= 0x0FFFFFFF;

		int s;
		int j = 0;

		for (i = 0; i < ROUNDS; i++) {
			if ((0x7EFC >> i & 1) == 1) {
				c = (c >>> 2 | c << 26) & 0x0FFFFFFF;
				d = (d >>> 2 | d << 26) & 0x0FFFFFFF;
			} else {
				c = (c >>> 1 | c << 27) & 0x0FFFFFFF;
				d = (d >>> 1 | d << 27) & 0x0FFFFFFF;
			}
			s = SKB[		   c		 & 0x3F						   ] |
				SKB[0x040 | (((c >>>  6) & 0x03) | ((c >>>	7) & 0x3C))] |
				SKB[0x080 | (((c >>> 13) & 0x0F) | ((c >>> 14) & 0x30))] |
				SKB[0x0C0 | (((c >>> 20) & 0x01) | ((c >>> 21) & 0x06)
												 | ((c >>> 22) & 0x38))];
			t = SKB[0x100 | ( d			& 0x3F						)] |
				SKB[0x140 | (((d >>>  7) & 0x03) | ((d >>>	8) & 0x3c))] |
				SKB[0x180 | ((d >>> 15) & 0x3F						)] |
				SKB[0x1C0 | (((d >>> 21) & 0x0F) | ((d >>> 22) & 0x30))];

			sKey[j++] = t <<  16 | (s & 0x0000FFFF);
			s		  = s >>> 16 | (t & 0xFFFF0000);
			sKey[j++] = s <<   4 |	s >>> 28;
		}
		return sKey;
	}

	private static int[] crypt3(int[] sKey, int E0, int E1) {
		int L = 0;
		int R = 0;
		int t, u, v;
		for (int i = 0; i < 25; i++) {
			for (int j = 0; j < ROUNDS * 2;) {
				v = R ^ (R >>> 16);
				u = v & E0;
				v &= E1;
				u ^= (u << 16) ^ R ^ sKey[j++];
				t = v ^ (v << 16) ^ R ^ sKey[j++];
				t = t >>> 4 | t << 28;
				L ^= (SP_TRANS[0x040 | ( t		   & 0x3F)] |
					  SP_TRANS[0x0C0 | ((t >>>	8) & 0x3F)] |
					  SP_TRANS[0x140 | ((t >>> 16) & 0x3F)] |
					  SP_TRANS[0x1C0 | ((t >>> 24) & 0x3F)] |
					  SP_TRANS[			 u		   & 0x3F ] |
					  SP_TRANS[0x080 | ((u >>>	8) & 0x3F)] |
					  SP_TRANS[0x100 | ((u >>> 16) & 0x3F)] |
					  SP_TRANS[0x180 | ((u >>> 24) & 0x3F)]);
					
				v = L ^ (L >>> 16);
				u = v & E0;
				v &= E1;
				u ^= (u << 16) ^ L ^ sKey[j++];
				t = v ^ (v << 16) ^ L ^ sKey[j++];
				t = t >>> 4 | t << 28;
				R ^= (SP_TRANS[0x040 | (t		  & 0x3F)] |
					  SP_TRANS[0x0C0 | ((t >>>	8) & 0x3F)] |
					  SP_TRANS[0x140 | ((t >>> 16) & 0x3F)] |
					  SP_TRANS[0x1C0 | ((t >>> 24) & 0x3F)] |
					  SP_TRANS[			 u		   & 0x3F ] |
					  SP_TRANS[0x080 | ((u >>>	8) & 0x3F)] |
					  SP_TRANS[0x100 | ((u >>> 16) & 0x3F)] |
					  SP_TRANS[0x180 | ((u >>> 24) & 0x3F)]);
			}
			t = L; L = R; R = t;
		}
		t = L;
		L = R >>> 1 | R << 31;
		R = t >>> 1 | t << 31;

		t = (R >>> 1 ^ L) & 0x55555555;
		L ^= t;
		R ^= t << 1;
		t = (L >>> 8 ^ R) & 0x00FF00FF;
		R ^= t;
		L ^= t << 8;
		t = (R >>> 2 ^ L) & 0x33333333;
		L ^= t;
		R ^= t << 2;
		t = (L >>> 16 ^ R) & 0x0000FFFF;
		R ^= t;
		L ^= t << 16;
		t = (R >>> 4 ^ L) & 0x0F0F0F0F;

		int[] result = {L ^ t, R ^ (t << 4)};
		return result;
	}

// Main
//...........................................................................

	/**
	 * Calculates the hash of a salt and password given on the command line.
	 * <p>
	 * Usage:
	 * <pre>
	 *	  java cryptix.tools.UnixCrypt [&lt;salt&gt;] &lt;clear-password&gt;
	 * </pre>
	 */
/*	public static void main(String[] args) {
		String salt = null;
		String original;

		switch (args.length) {
			case 2:
				salt = args[0];
				original = args[1];
				break;

			case 1:
				salt = "";
				original = args[0];
				break;

			default:
				System.out.println(
					"Usage:\n" +
					"	 java cryptix.tools.UnixCrypt [<salt>] <clear-password>");
				self_test();
				return;
		}
		try {
			System.out.print(
				"[" + (salt + "AA").substring(0, 2) + "] " +
				"[" + original + "] => ");
			System.out.println(
				"[" + UnixCrypt.crypt(original, salt) + "]");
		} catch (Exception e) {
			e.printStackTrace();
		}

	}*/

	/** Test that is run by distribution to make sure everything is OK! */
	/*
	 * This C test program will confirm (note that some systems
	 * don't implement straight crypt(3)).
	 *	
	 * #include <unistd.h>
	 * main()
	 * {
	 *	   const char *key = "CryptixRulez";
	 *	   const char salt[] = {'o','k'};
	 *	   printf("crypt(%s, %s) = %s\n",
	 *			  key, salt, crypt(key, salt));
	 * }
	 */
/*	private static void self_test() {
		String original = "CryptixRulez";
		String salt = "OK";
		String solution = "OKDvOv8WCyJBI";
		System.out.println("Selftest:");

	try
	{
			String crypted = UnixCrypt.crypt(original, salt);
			if (!solution.equals(crypted)) {
				System.out.println( "self_test: " + solution + " != " + crypted);
				System.exit(1);
			}
			System.out.println("	" + original + " " + salt + ": " + crypted);
		} catch (Exception e) {
			e.printStackTrace();
	}
	}*/
}
