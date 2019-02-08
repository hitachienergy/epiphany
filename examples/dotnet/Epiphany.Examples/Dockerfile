FROM microsoft/dotnet:2.2-aspnetcore-runtime AS base
WORKDIR /app
EXPOSE 3109
EXPOSE 44387

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples/Epiphany.Examples.Api.csproj Epiphany.Examples/
RUN dotnet restore Epiphany.Examples/Epiphany.Examples.Api.csproj
COPY . .
WORKDIR /src/Epiphany.Examples
RUN dotnet build Epiphany.Examples.Api.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.Api.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.Api.dll"]
