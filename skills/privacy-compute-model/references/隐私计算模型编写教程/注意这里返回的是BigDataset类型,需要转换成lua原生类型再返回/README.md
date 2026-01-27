# 注意这里返回的是BigDataset类型,需要转换成lua原生类型再返回

---

## 主内容

# 注意这里返回的是BigDataset类型,需要转换成lua原生类型再返回
	bds=fccall.psiInvoke(p1,p2)
    return bds:loadAll()
end

```
