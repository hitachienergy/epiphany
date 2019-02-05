namespace Epiphany.Examples.Messaging
{
    public interface ISerializer
    {
        string Serialize<T>(T model);
    }
}
