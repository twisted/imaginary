
package twisted.util.parse;

public interface Token
{
	Token next();
	int type();
	Object data();
}
