FROM microsoft/dotnet:2.2-aspnetcore-runtime AS base
WORKDIR /app
EXPOSE 80

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples.Web/Epiphany.Examples.Web.csproj Epiphany.Examples.Web/
RUN dotnet restore Epiphany.Examples.Web/Epiphany.Examples.Web.csproj
COPY . .
WORKDIR /src/Epiphany.Examples.Web
RUN dotnet build Epiphany.Examples.Web.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.Web.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.Web.dll"]
