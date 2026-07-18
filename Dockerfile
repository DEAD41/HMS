FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY artifacts/api/ .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "HealthcareERP.Api.dll"]
