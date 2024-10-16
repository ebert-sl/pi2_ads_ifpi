from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from db import get_session, init_db
from models import Montadora, ModeloVeiculo, Veiculo

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/montadoras")
async def list_montadoras(request: Request, session: Session = Depends(get_session)):
    montadoras = session.query(Montadora).all()
    return templates.TemplateResponse("montadora_list.html", {"request": request, "montadoras": montadoras})

@app.get("/montadoras/create")
async def create_montadora_form(request: Request):
    return templates.TemplateResponse("montadora_create.html", {"request": request})

@app.post("/montadoras/create")
async def create_montadora(request: Request, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...), session: Session = Depends(get_session)):
    nova_montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano_fundacao)
    session.add(nova_montadora)
    session.commit()
    session.refresh(nova_montadora)
    return templates.TemplateResponse("montadora_create.html", {"request": request, "success": True})

@app.get("/montadoras/edit/{id}")
async def edit_montadora_form(request: Request, id: int, session: Session = Depends(get_session)):
    montadora = session.get(Montadora, id)
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    return templates.TemplateResponse("montadora_edit.html", {"request": request, "montadora": montadora})

@app.post("/montadoras/edit/{id}")
async def edit_montadora(request: Request, id: int, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...), session: Session = Depends(get_session)):
    montadora = session.get(Montadora, id)
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    
    montadora.nome = nome
    montadora.pais = pais
    montadora.ano_fundacao = ano_fundacao

    session.add(montadora)
    session.commit()
    session.refresh(montadora)
    return templates.TemplateResponse("montadora_edit.html", {"request": request, "success": True, "montadora": montadora})

@app.post("/montadoras/delete/{id}")
async def delete_montadora(id: int, session: Session = Depends(get_session)):
    montadora = session.get(Montadora, id)
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    
    session.delete(montadora)
    session.commit()

    return RedirectResponse(url="/montadoras?deleted=True", status_code=303)

@app.get("/modelos_veiculo")
async def list_modelos_veiculo(request: Request, session: Session = Depends(get_session)):
    modelos = session.exec(
        select(ModeloVeiculo, Montadora).join(Montadora, ModeloVeiculo.montadora_id == Montadora.id)
    ).all()
    modelos_completos = [
        {
            "modelo": modelo,
            "montadora": montadora
        }
        for modelo, montadora in modelos
    ]
    return templates.TemplateResponse("modelo_veiculo_list.html", {"request": request, "modelos": modelos_completos})

@app.get("/modelos_veiculo/create")
async def create_modelo_veiculo_form(request: Request, session: Session = Depends(get_session)):
    montadoras = session.query(Montadora).all()
    return templates.TemplateResponse("modelo_veiculo_create.html", {"request": request, "montadoras": montadoras})

@app.post("/modelos_veiculo/create")
async def create_modelo_veiculo(request: Request, nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...), motorizacao: float = Form(...), turbo: bool = Form(False), automatico: bool = Form(False), session: Session = Depends(get_session)):
    novo_modelo = ModeloVeiculo(nome=nome, montadora_id=montadora_id, valor_referencia=valor_referencia, motorizacao=motorizacao, turbo=turbo, automatico=automatico)
    session.add(novo_modelo)
    session.commit()
    session.refresh(novo_modelo)
    montadoras = session.query(Montadora).all()
    return templates.TemplateResponse("modelo_veiculo_create.html", {"request": request, "success": True, "montadoras": montadoras})

@app.get("/modelos_veiculo/edit/{id}")
async def edit_modelo_veiculo_form(request: Request, id: int, session: Session = Depends(get_session)):
    modelo = session.get(ModeloVeiculo, id)
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo de Veículo não encontrado")
    montadoras = session.query(Montadora).all()
    return templates.TemplateResponse("modelo_veiculo_edit.html", {"request": request, "modelo": modelo, "montadoras": montadoras})

@app.post("/modelos_veiculo/edit/{id}")
async def edit_modelo_veiculo(request: Request, id: int, nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...), motorizacao: float = Form(...), turbo: bool = Form(False), automatico: bool = Form(False), session: Session = Depends(get_session)):
    modelo = session.get(ModeloVeiculo, id)
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo de Veículo não encontrado")
    
    modelo.nome = nome
    modelo.montadora_id = montadora_id
    modelo.valor_referencia = valor_referencia
    modelo.motorizacao = motorizacao
    modelo.turbo = turbo
    modelo.automatico = automatico

    session.add(modelo)
    session.commit()
    session.refresh(modelo)
    montadoras = session.query(Montadora).all()
    return templates.TemplateResponse("modelo_veiculo_edit.html", {"request": request, "success": True, "modelo": modelo, "montadoras": montadoras})

@app.post("/modelos_veiculo/delete/{id}")
async def delete_modelo_veiculo(id: int, session: Session = Depends(get_session)):
    modelo = session.get(ModeloVeiculo, id)
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo de Veículo não encontrado")
    
    session.delete(modelo)
    session.commit()

    return RedirectResponse(url="/modelos_veiculo?deleted=True", status_code=303)

@app.get("/veiculos")
async def list_veiculos(request: Request, session: Session = Depends(get_session)):
    veiculos = session.exec(
        select(Veiculo, ModeloVeiculo)
        .join(ModeloVeiculo, Veiculo.modelo_id == ModeloVeiculo.id)
    ).all()
    veiculos_completos = [
        {
            "veiculo": veiculo,
            "modelo": modelo
        }
        for veiculo, modelo in veiculos
    ]
    return templates.TemplateResponse("veiculo_list.html", {"request": request, "veiculos": veiculos_completos})

@app.get("/veiculos/create")
async def create_veiculo_form(request: Request, session: Session = Depends(get_session)):
    modelos = session.query(ModeloVeiculo).all()
    return templates.TemplateResponse("veiculo_create.html", {"request": request, "modelos": modelos})

@app.post("/veiculos/create")
async def create_veiculo(request: Request, modelo_id: int = Form(...), cor: str = Form(...), ano_fabricacao: int = Form(...), ano_modelo: int = Form(...), valor: float = Form(...), placa: str = Form(...), vendido: bool = Form(False), session: Session = Depends(get_session)):
    novo_veiculo = Veiculo(modelo_id=modelo_id, cor=cor, ano_fabricacao=ano_fabricacao, ano_modelo=ano_modelo, valor=valor, placa=placa, vendido=vendido)
    session.add(novo_veiculo)
    session.commit()
    session.refresh(novo_veiculo)
    modelos = session.query(ModeloVeiculo).all()
    return templates.TemplateResponse("veiculo_create.html", {"request": request, "success": True, "modelos": modelos})

@app.get("/veiculos/edit/{id}")
async def edit_veiculo_form(request: Request, id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    modelos = session.query(ModeloVeiculo).all()
    return templates.TemplateResponse("veiculo_edit.html", {"request": request, "veiculo": veiculo, "modelos": modelos})

@app.post("/veiculos/edit/{id}")
async def edit_veiculo(request: Request, id: int, modelo_id: int = Form(...), cor: str = Form(...), ano_fabricacao: int = Form(...), ano_modelo: int = Form(...), valor: float = Form(...), placa: str = Form(...), vendido: bool = Form(False), session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    veiculo.modelo_id = modelo_id
    veiculo.cor = cor
    veiculo.ano_fabricacao = ano_fabricacao
    veiculo.ano_modelo = ano_modelo
    veiculo.valor = valor
    veiculo.placa = placa
    veiculo.vendido = vendido

    session.add(veiculo)
    session.commit()
    session.refresh(veiculo)
    modelos = session.query(ModeloVeiculo).all()
    return templates.TemplateResponse("veiculo_edit.html", {"request": request, "success": True, "veiculo": veiculo, "modelos": modelos})

@app.post("/veiculos/delete/{id}")
async def delete_veiculo(id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    session.delete(veiculo)
    session.commit()

    return RedirectResponse(url="/veiculos?deleted=True", status_code=303)